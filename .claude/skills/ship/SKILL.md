---
name: ship
description: Run a gated four-agent G-PROJECT development task with Unreal tests and visual evidence.
disable-model-invocation: true
---

Feature request: $ARGUMENTS

This skill is manually invoked with /ship <one small feature>. No unattended merge, push, deletion, or deployment.

1. Read CLAUDE.md and Tools/AIDevTeam/README.md. Confirm the current directory is G-PROJECT. Inspect git status, branch, and actual project files. If the request is empty, the working tree contains unrelated changes, or the root is unclear, stop without touching production code.
2. Ensure the feature runs on a dedicated non-main Git branch. If currently on main and clean, create a fresh ai/ship-<timestamp> branch; otherwise use the already isolated feature branch. Never reset, stash, delete, or commit any existing user files.
3. Call the local Python interpreter (Windows: py -3, otherwise python) to run Tools/AIDevTeam/pipeline.py start --request "<the exact feature request>". Capture the printed RUN_ID and RUN_DIR. Use this new run throughout; never recycle old .pipeline output.
4. Delegate to gp-planner with the exact request and RUN_DIR. Wait for spec.md. Run Tools/AIDevTeam/pipeline.py check --run <RUN_ID> --stage plan; stop if it fails or any questions remain.
5. Delegate to gp-coder with RUN_DIR. Wait for changes.md. Run the same check with --stage code; stop on failure.
6. Delegate to gp-tester with RUN_DIR. Wait for test-results.md. Run the check with --stage test; stop on any failed, blocked, skipped, or missing mandatory verification.
7. Gather git status, git diff, newly created files, the full plan, tests, and screenshot evidence. Delegate to gp-reviewer with these inputs. Do not let the reviewer edit anything. Write the reviewer's verdict response exactly to RUN_DIR/review.md, without upgrading or sanitizing it. Run pipeline.py check --run <RUN_ID> --stage review.
8. Report the branch, RUN_DIR, tests actually run, screenshots/reference views, remaining blockers and verdict. READY_FOR_OWNER_REVIEW is NOT a shipped feature. Ask the owner for visual acceptance when required. Never merge, push, or auto-approve.

If Python, Claude agent delegation, Git, Unreal Editor, or required reference content is unavailable, report the specific blocker rather than pretending the pipeline succeeded. Start with small pilots, such as a read-only improvement to Tools/TreeProductionDashboard.
