#!/usr/bin/env python3
"""Run a real UE 5.8 automation filter and fail closed on missing/skipped tests.

No shell, package creation, Unreal content modification, or background processes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def evaluate_report(path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, "Epic automation index.json was not produced."
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        counts = {name: int(data.get(name, -1)) for name in
                  ("succeeded", "succeededWithWarnings", "failed", "notRun", "inProcess")}
        tests = data.get("tests", [])
        passed = (counts["succeeded"] > 0 and
                  all(counts[key] == 0 for key in
                      ("succeededWithWarnings", "failed", "notRun", "inProcess")) and
                  bool(tests) and
                  all(str(test.get("state", "")).lower() == "success" for test in tests))
        return passed, "Counts: " + json.dumps(counts) + "; test entries: " + str(len(tests))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        return False, "Invalid Unreal JSON report: " + str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Existing .uproject file")
    parser.add_argument("--engine-root", default=os.getenv("UE_ROOT", ""),
                        help="UE install root (or use UE_ROOT environment variable)")
    parser.add_argument("--editor", default="", help="Optional exact UnrealEditor-Cmd.exe path")
    parser.add_argument("--run-dir", required=True, help="Current isolated .pipeline run")
    parser.add_argument("--filter", required=True, help="Existing Epic Automation test path/group")
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--dry-run", action="store_true", help="Print command; never mark passed")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    run_dir = Path(args.run_dir).expanduser().resolve()
    if not project.is_file() or project.suffix.lower() != ".uproject":
        parser.error("Provide a real existing .uproject path.")
    if not run_dir.is_dir():
        parser.error("RUN_DIR must already exist.")
    if not re.fullmatch(r"[A-Za-z0-9_ .:+-]+", args.filter):
        parser.error("Unsafe filter; use an existing test path/group, not console commands.")
    if args.timeout_seconds < 1:
        parser.error("Timeout must be greater than zero.")

    if args.editor:
        editor = Path(args.editor).expanduser().resolve()
    elif args.engine_root:
        editor = Path(args.engine_root).expanduser().resolve() / "Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
    else:
        editor = Path(r"C:\Program Files\Epic Games\UE_5.8") / "Engine/Binaries/Win64/UnrealEditor-Cmd.exe"

    report_dir = run_dir / "unreal-report"
    command = [str(editor), str(project), "-unattended", "-nop4", "-nosplash",
               "-ExecCmds=Automation RunTests " + args.filter + ";Quit",
               "-TestExit=Automation Test Queue Empty",
               "-ReportOutputPath=" + str(report_dir), "-log"]
    print("Unreal command:", subprocess.list2cmdline(command) if os.name == "nt"
          else shlex.join(command))
    if args.dry_run:
        print("DRY RUN ONLY: no tests executed and no PASS status issued.")
        return 0
    if not editor.is_file():
        parser.error("UnrealEditor-Cmd.exe not found at " + str(editor))

    if report_dir.exists():
        parser.error("A report directory already exists for this run. Create a fresh RUN_ID.")
    report_dir.mkdir(parents=True, exist_ok=False)
    log_file = run_dir / "unreal-output.log"
    exit_code: int | None = None
    error: str | None = None
    try:
        with log_file.open("w", encoding="utf-8") as log:
            process = subprocess.run(command, cwd=str(project.parent),
                                     stdout=log, stderr=subprocess.STDOUT,
                                     timeout=args.timeout_seconds, check=False)
            exit_code = process.returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        error = str(exc)
    report_file = report_dir / "index.json"
    if not report_file.is_file():
        report_file = report_dir / "Index.json"
    passed_report, detail = evaluate_report(report_file)
    passed = (exit_code == 0 and passed_report and error is None)
    summary = {
        "project": str(project), "editor": str(editor), "filter": args.filter,
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": False, "exit_code": exit_code, "passed": passed,
        "report": str(report_file), "log": str(log_file),
        "details": detail, "error": error,
    }
    (run_dir / "unreal-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("Unreal automation:", "PASS" if passed else "FAIL")
    print("Log:", log_file)
    print("Report:", report_file)
    print(detail)
    if error:
        print(error, file=sys.stderr)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
