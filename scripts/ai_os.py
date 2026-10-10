#!/usr/bin/env python3
"""G-PROJECT's offline, stdlib-only memory audit, skill router and lesson ledger."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / ".ai-os-data"
AREAS = ROOT / "AI_OS" / "areas"
SECTIONS = ["Projects", "State", "Skills", "Memory", "Routines", "Not here"]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WORD = re.compile(r"[a-z0-9]+")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def registry(root: Path = ROOT) -> list[dict]:
    data = read_json(root / "AI_OS" / "skill_registry.json")
    return data["skills"]


def audit(root: Path = ROOT) -> list[str]:
    """Pure read-only validation. Return actionable errors, never change files."""
    errors = []
    master = root / "AI_OS" / "MAP.md"
    areas = root / "AI_OS" / "areas"
    documents = [master, *sorted(areas.glob("*.md"))] if areas.exists() else [master]
    if len(documents) < 2:
        errors.append("AI_OS/areas must have at least one signpost")
    for doc in documents:
        rel = doc.relative_to(root).as_posix()
        if not doc.is_file():
            errors.append(f"Missing signpost: {rel}")
            continue
        content = doc.read_text(encoding="utf-8")
        lines = content.splitlines()
        if len(lines) > (60 if doc == master else 80):
            errors.append(f"{rel}: too many lines")
        if doc != master:
            headings = re.findall(r"^## (.+)$", content, flags=re.MULTILINE)
            if headings != SECTIONS:
                errors.append(f"{rel}: expected six ordered sections: {SECTIONS}")
        for href in LINK.findall(content):
            ref = href.split("#", 1)[0]
            if not ref or re.match(r"^[a-z][a-z0-9+.-]*://", ref, re.I):
                continue
            target = (doc.parent / ref).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{rel}: link escapes repo: {href}")
                continue
            if not target.exists():
                errors.append(f"{rel}: broken link {href}")
    try:
        records = registry(root)
    except (OSError, ValueError, KeyError) as exc:
        return errors + [f"Invalid skill registry: {exc}"]
    ids = set()
    for item in records:
        sid, relative = item.get("id", ""), item.get("path", "")
        if not sid or sid in ids:
            errors.append(f"Skill ID missing or duplicate: {sid}")
        ids.add(sid)
        if not item.get("triggers"):
            errors.append(f"Skill {sid} has no triggers")
        path = (root / relative).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"Skill {sid} escapes repo")
            continue
        if not path.is_file():
            errors.append(f"Skill {sid} has missing SKILL.md: {relative}")
            continue
        body = path.read_text(encoding="utf-8")
        if not body.startswith("---\n") or "\n---\n" not in body[4:]:
            errors.append(f"Skill {sid}: missing YAML frontmatter")
        elif not re.search(r"^description:\s*\S", body, re.MULTILINE):
            errors.append(f"Skill {sid}: missing description")
    return errors


def route(query: str, records: list[dict]) -> list[dict]:
    text = " ".join(WORD.findall(query.lower()))
    choices = []
    for item in records:
        hits = []
        for phrase in item.get("triggers", []):
            normalized = " ".join(WORD.findall(phrase.lower()))
            if normalized and re.search(r"(?<!\w)" + re.escape(normalized) + r"(?!\w)", text):
                hits.append(normalized)
        if hits:
            score = max(len(h.split()) * 100 + len(h) for h in hits)
            score += min(len(hits), 4) * 10 + int(item.get("priority", 0))
            choices.append({"skill": item["id"], "path": item["path"],
                            "score": score, "matched": sorted(set(hits))})
    return sorted(choices, key=lambda x: (-x["score"], x["skill"]))


def store_path(store: str | None = None) -> Path:
    return Path(store or os.environ.get("AI_OS_DATA_DIR") or DATA).expanduser().resolve()


def read_lessons(store: Path) -> list[dict]:
    filename = store / "lessons.jsonl"
    if not filename.is_file():
        return []
    lessons = []
    with filename.open(encoding="utf-8") as handle:
        for n, line in enumerate(handle, start=1):
            if line.strip():
                try:
                    lessons.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Corrupt {filename.name} line {n}: {exc}") from exc
    return lessons


def learn(store: Path, task: str, symptom: str, cause: str, remedy: str,
          proof: str, skill: str, kind: str = "failure", confidence: str = "unverified",
          known_skills: set[str] | None = None) -> dict:
    if known_skills is not None and skill not in known_skills:
        raise ValueError(f"Unknown skill '{skill}'")
    if confidence == "verified" and proof.casefold() in {"unverified", "unknown", "none", ""}:
        raise ValueError("Verified lessons require actual evidence in --proof")
    if any(not v.strip() for v in (task, symptom, cause, remedy, proof, skill)):
        raise ValueError("All lesson fields must be nonempty")
    record = {"id": str(uuid.uuid4()), "at": datetime.now(timezone.utc).isoformat(),
              "kind": kind, "confidence": confidence, "task": task, "symptom": symptom,
              "cause": cause, "remedy": remedy, "proof": proof, "skill": skill}
    store.mkdir(parents=True, exist_ok=True)
    with (store / "lessons.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return record


def recall(query: str, lessons: list[dict], limit: int = 5) -> list[dict]:
    terms = {t for t in WORD.findall(query.lower()) if len(t) > 2}
    matches = []
    for rec in lessons:
        index = " ".join(str(rec.get(k, "")) for k in
                         ("task", "symptom", "cause", "remedy", "skill")).lower()
        words = set(WORD.findall(index))
        count = len(terms & words)
        if count or not terms:
            matches.append((count, rec))
    matches.sort(key=lambda pair: pair[1].get("at", ""), reverse=True)
    matches.sort(key=lambda pair: pair[0], reverse=True)
    return [rec for _, rec in matches[:limit]]


def propose(store: Path, lesson_id: str, known_skills: dict[str, str]) -> Path:
    lesson = next((item for item in read_lessons(store) if item.get("id") == lesson_id), None)
    if lesson is None:
        raise ValueError(f"No lesson with ID {lesson_id}")
    skill = lesson["skill"]
    if skill not in known_skills:
        raise ValueError(f"Unknown skill {skill}")
    # A proposal is never an automatic skill rewrite.
    path = store / "proposals" / f"{lesson_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Proposal already exists: {path}")
    text = (f"# Candidate improvement for {skill}\n\n"
            f"Status: NEEDS REVIEW, NOT APPLIED\n"
            f"Target: {known_skills[skill]}\n"
            f"Lesson ID: {lesson_id}\n\n"
            f"Observed symptom: {lesson['symptom']}\n\n"
            f"Hypothesized cause: {lesson['cause']}\n\n"
            f"Suggested correction: {lesson['remedy']}\n\n"
            f"Evidence: {lesson['proof']} ({lesson['confidence']})\n\n"
            "Acceptance checklist:\n"
            "- [ ] Owner checks evidence and approves the scope.\n"
            "- [ ] Update ONE trigger/process/guardrail in the target skill.\n"
            "- [ ] Add a negative regression case and a golden success example.\n"
            "- [ ] Run deterministic tests and Unreal visual/audio test if relevant.\n"
            "- [ ] Reviewer approves; owner signs off before promotion.\n")
    path.write_text(text, encoding="utf-8")
    return path


def cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Audit memory links, signposts and skill metadata")
    r = commands.add_parser("route", help="Return ranked skill choices for a task")
    r.add_argument("task", help="Task description")
    rc = commands.add_parser("recall", help="Search local mistake and success history")
    rc.add_argument("query")
    rc.add_argument("--store", default=None)
    rc.add_argument("--limit", type=int, default=5)
    l = commands.add_parser("learn", help="Append an observed lesson to local-only ledger")
    for field in ("task", "symptom", "cause", "remedy", "proof", "skill"):
        l.add_argument("--" + field, required=True)
    l.add_argument("--kind", choices=("failure", "success"), default="failure")
    l.add_argument("--confidence", choices=("verified", "unverified"), default="unverified")
    l.add_argument("--store", default=None)
    p = commands.add_parser("propose", help="Create private review proposal (never edits skill)")
    p.add_argument("--id", required=True)
    p.add_argument("--store", default=None)
    args = parser.parse_args()
    try:
        if args.command == "check":
            problems = audit()
            if problems:
                print("\n".join("FAIL: " + problem for problem in problems))
                return 1
            print("PASS: memory map, signposts and skill registry")
        elif args.command == "route":
            choices = route(args.task, registry())
            print(json.dumps(choices[:5], indent=2))
            if not choices:
                print("No automatic match: read AI_OS/MAP.md and choose manually.")
        elif args.command == "recall":
            print(json.dumps(recall(args.query, read_lessons(store_path(args.store)), args.limit), indent=2))
        elif args.command == "learn":
            record = learn(store_path(args.store), args.task, args.symptom, args.cause,
                           args.remedy, args.proof, args.skill, args.kind, args.confidence,
                           {item["id"] for item in registry()})
            print(json.dumps(record, indent=2))
        elif args.command == "propose":
            registered = {item["id"]: item["path"] for item in registry()}
            print(propose(store_path(args.store), args.id, registered))
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(cli())
