#!/usr/bin/env python3
"""One bounded MAPS Pulse routine: a read-only memory-map audit.

Manual-only; no AI calls, networking, schedules, git mutation, or publishing.
Appends local records only under ignored .pipeline/pulse.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from memory_check import ROOT, verify_map

DAY_LIMIT = 12
ROLLING_HOUR_LIMIT = 2
ROUTINE = "memory-audit"


def history_file(root: Path, day: str) -> Path:
    return root / ".pipeline" / "pulse" / ("runs-" + day + ".jsonl")


def prior_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError("not a record")
            records.append(record)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"Invalid run log line {number}; stop rather than ignore it: {exc}") from exc
    return records


def allowed(root: Path, now: datetime) -> tuple[bool, str]:
    today = history_file(root, now.date().isoformat())
    yesterday = history_file(root, (now - timedelta(days=1)).date().isoformat())
    todays_records = prior_records(today)
    relevant = todays_records + prior_records(yesterday)
    recent = []
    for record in relevant:
        if record.get("routine") != ROUTINE:
            continue
        try:
            timestamp = datetime.fromisoformat(record["started_utc"].replace("Z", "+00:00"))
        except (KeyError, AttributeError, ValueError) as exc:
            raise ValueError("Missing or invalid started_utc in Pulse history.") from exc
        if timestamp.tzinfo is None:
            raise ValueError("Pulse timestamp is missing timezone.")
        if now - timedelta(hours=1) < timestamp <= now:
            recent.append(record)
    if sum(item.get("routine") == ROUTINE for item in todays_records) >= DAY_LIMIT:
        return False, f"Daily ceiling reached ({DAY_LIMIT})."
    if len(recent) >= ROLLING_HOUR_LIMIT:
        return False, f"Rolling hour ceiling reached ({ROLLING_HOUR_LIMIT})."
    return True, "Caps permit one read-only memory audit."


def run_audit(root: Path) -> int:
    now = datetime.now(timezone.utc)
    folder = root / ".pipeline" / "pulse"
    folder.mkdir(parents=True, exist_ok=True)
    lock = folder / ".memory-audit.lock"
    try:
        lock_fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        print("PULSE BLOCKED: another memory audit owns the local lock.", file=sys.stderr)
        return 2
    try:
        os.close(lock_fd)
        ok, reason = allowed(root, now)
        if not ok:
            print("PULSE BLOCKED:", reason, file=sys.stderr)
            return 2
        result = verify_map(root)
        record = {
            "started_utc": now.isoformat(), "routine": ROUTINE, "machine": socket.gethostname(),
            "model": None, "model_calls": 0, "turns": 0, "cost_usd": 0,
            "status": "pass" if result["ok"] else "fail",
            "area_count": result["areas"], "document_count": result["documents"],
            "issues": result["issues"],
        }
        with history_file(root, now.date().isoformat()).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(json.dumps(record, indent=2))
        return 0 if result["ok"] else 1
    finally:
        # Only this function holds the exclusive lock.
        lock.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true", help="Validate map without writing history")
    args = parser.parse_args()
    try:
        if args.dry_run:
            report = verify_map(args.root)
            print("Dry-run memory audit:", "PASS" if report["ok"] else "FAIL")
            for issue in report["issues"]:
                print(" -", issue)
            return 0 if report["ok"] else 1
        return run_audit(args.root)
    except (ValueError, OSError) as exc:
        print("PULSE FAILED:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
