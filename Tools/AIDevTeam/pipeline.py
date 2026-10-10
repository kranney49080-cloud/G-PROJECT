#!/usr/bin/env python3
"""Isolated handoffs and objective gates for the G-PROJECT Claude development team.

Standard library only. A report means READY FOR OWNER REVIEW, never an auto-merge.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
RUN_ID_PATTERN = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[a-z0-9-]+-[0-9a-f]{6}$")
FIELDS = re.compile(r"^([A-Z_]+):[ \t]*(.*?)\s*$", re.MULTILINE)


class GateError(Exception):
    """A missing or failed stage artifact."""


def fields_from(text: str) -> dict[str, str]:
    return dict(FIELDS.findall(text))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def create_run(root: Path, request: str) -> str:
    request = request.strip()
    require(bool(request), "Feature request must not be empty.")
    slug = re.sub(r"[^a-z0-9]+", "-", request.lower()).strip("-")[:30].strip("-")
    slug = slug or "feature"
    run_id = (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
              + "-" + slug + "-" + secrets.token_hex(3))
    run_dir = root / ".pipeline" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "request.md").write_text("# Feature request\n\n" + request + "\n", encoding="utf-8")
    (run_dir / "run.json").write_text(
        json.dumps({"run_id": run_id, "request": request, "created_utc":
                    datetime.now(timezone.utc).isoformat()}, indent=2) + "\n",
        encoding="utf-8",
    )
    return run_id


def get_run_dir(root: Path, run_id: str) -> Path:
    require(bool(RUN_ID_PATTERN.fullmatch(run_id)), "Invalid run ID.")
    path = root / ".pipeline" / "runs" / run_id
    require(path.is_dir(), "Run directory does not exist: " + str(path))
    return path


def read_artifact(run_dir: Path, name: str) -> tuple[str, dict[str, str]]:
    path = run_dir / name
    require(path.is_file(), "Missing artifact: " + str(path))
    text = path.read_text(encoding="utf-8")
    return text, fields_from(text)


def evidence_image(run_dir: Path, relative: str) -> Path:
    require(bool(relative), "A mandatory evidence image path is empty.")
    image = (run_dir / relative).resolve()
    root = run_dir.resolve()
    require(image.is_relative_to(root), "Evidence must be inside RUN_DIR: " + relative)
    require(image.is_file(), "Missing evidence image: " + str(image))
    require(image.suffix.lower() in (".png", ".jpg", ".jpeg"), "Evidence must be PNG or JPEG.")
    prefix = image.open("rb").read(8)
    require(prefix.startswith(b"\x89PNG\r\n\x1a\n") or prefix.startswith(b"\xff\xd8\xff"),
            "Evidence file is not a recognized PNG/JPEG: " + relative)
    return image


def check_unreal(run_dir: Path) -> None:
    summary_file = run_dir / "unreal-summary.json"
    require(summary_file.is_file(), "Unreal test summary is missing.")
    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    require(summary.get("passed") is True and summary.get("dry_run") is False,
            "Real Unreal automation did not pass.")
    report = run_dir / "unreal-report" / "index.json"
    if not report.is_file():
        report = run_dir / "unreal-report" / "Index.json"
    require(report.is_file(), "Epic automation index.json report is missing.")
    data = json.loads(report.read_text(encoding="utf-8"))
    require(int(data.get("succeeded", 0)) > 0, "Unreal report has no successful tests.")
    for key in ("failed", "notRun", "inProcess", "succeededWithWarnings"):
        require(int(data.get(key, -1)) == 0, "Unreal report requires zero " + key + ".")
    tests = data.get("tests", [])
    require(bool(tests), "Unreal report contains no executed tests.")
    require(all(str(item.get("state", "")).lower() == "success" for item in tests),
            "Unreal report includes non-successful or skipped tests.")


def check_run(root: Path, run_id: str, stage: str) -> str:
    run_dir = get_run_dir(root, run_id)
    _, spec = read_artifact(run_dir, "spec.md")
    require(spec.get("OPEN_QUESTIONS") == "NONE", "Planner left open questions.")
    for key in ("UNREAL_REQUIRED", "VISUAL_REQUIRED"):
        require(spec.get(key) in ("YES", "NO"), "Spec missing " + key + ": YES/NO.")
    if stage == "plan":
        return "PLAN PASS"

    changes_text, changes = read_artifact(run_dir, "changes.md")
    require(changes.get("STATUS") == "IMPLEMENTED", "Coder did not complete implementation.")
    require("FILES_CHANGED:" in changes_text and re.search(r"(?m)^-\s+\S", changes_text),
            "Changes summary has no changed-file list.")
    if stage == "code":
        return "CODE PASS"

    _, tests = read_artifact(run_dir, "test-results.md")
    require(tests.get("RESULT") == "PASS", "Tests failed or were blocked.")
    try:
        count = int(tests.get("TESTS_RUN", "0"))
    except ValueError as exc:
        raise GateError("TESTS_RUN must be an integer.") from exc
    require(count > 0, "No tests actually executed.")
    require(bool(tests.get("COMMANDS")), "Test commands are missing.")
    log_value = tests.get("OUTPUT_LOG", "")
    require(bool(log_value), "Test log path is missing.")
    log_path = Path(log_value)
    if not log_path.is_absolute():
        log_path = run_dir / log_path
    require(log_path.is_file(), "The recorded test log file does not exist.")
    if spec["UNREAL_REQUIRED"] == "YES":
        require(tests.get("UNREAL_RESULTS") == "PASS", "Unreal result is not PASS.")
        check_unreal(run_dir)
    if spec["VISUAL_REQUIRED"] == "YES":
        _, evidence = read_artifact(run_dir, "evidence.md")
        require(evidence.get("EVIDENCE_STATUS") == "READY", "Visual evidence not ready.")
        before = evidence_image(run_dir, evidence.get("BEFORE_IMAGE", ""))
        after = evidence_image(run_dir, evidence.get("AFTER_IMAGE", ""))
        require(hashlib.sha256(before.read_bytes()).digest()
                != hashlib.sha256(after.read_bytes()).digest(),
                "Before and after images are byte-identical; provide real visual comparison.")
        require(bool(evidence.get("REFERENCE")), "Visual reference path/link is missing.")
        require(bool(evidence.get("CAMERA_VIEWS")), "Camera-view description is missing.")
    if stage == "test":
        return "TEST PASS (owner visual acceptance still required where relevant)"

    _, review = read_artifact(run_dir, "review.md")
    require(review.get("VERDICT") == "READY_FOR_OWNER_REVIEW",
            "Independent reviewer did not approve owner-review readiness.")
    return "READY FOR OWNER REVIEW (not merged or owner-approved)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Git repo root")
    sub = parser.add_subparsers(dest="operation", required=True)
    create = sub.add_parser("start", help="Create isolated feature run")
    create.add_argument("--request", required=True)
    check = sub.add_parser("check", help="Validate stage handoff and requirements")
    check.add_argument("--run", required=True)
    check.add_argument("--stage", choices=("plan", "code", "test", "review"), required=True)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.operation == "start":
            run_id = create_run(root, args.request)
            print("RUN_ID=" + run_id)
            print("RUN_DIR=" + str(get_run_dir(root, run_id)))
        else:
            print(check_run(root, args.run, args.stage))
        return 0
    except (GateError, OSError, json.JSONDecodeError) as exc:
        print("GATE FAILED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
