# G-PROJECT AI Development Team (Phase 1)

This is a **working, testable orchestration scaffold** for Claude Code with four project-scoped subagents:
gp-planner (Opus), gp-coder (Sonnet), gp-tester (Sonnet), gp-reviewer (Opus).

The source inspiration is Ray Fu's four-agent Claude Code workflow; we have adapted the design for G-PROJECT and added a machine-checkable gate script instead of claiming the tutorial's files are installed. The second reference is Pav Rusovs' free MAPS guide (`Memory, Agent, Pulse, Screen`): https://github.com/pavrus117/ai-os-maps-guide . We take its source-of-truth-as-owned-files, two-hop signposts, bounded routine and read-only screen principles. These are **independent starting references**, not copied implementations.

## Present state

- **Agent**: four project agents and an owner-invoked `/ship` skill exist under `.claude/`.
- **Memory**: `Tools/AIDevTeam/memory/MAP.md` links to four area signposts and existing files; check with `memory_check.py`.
- **Pulse**: `pulse.py` supports a *manual* read-only memory audit and local JSONL run history with daily/rolling caps. **No unattended schedule is installed.**
- **Screen**: planned for a later phase, once records and memory are useful. Screen must only read canonical records.
- **Unreal**: real UE automation helper is included, but no existing `.uproject` or UE 5.8 executable path has been confirmed via this repository. Do not claim Unreal tests passed.
- **Git**: no automatic commit, Git push, PR merge or removal. Owner retains approval.

## Setup on Windows

1. Work on a disposable feature branch with a **clean working tree**. Clone or pull G-PROJECT from GitHub before starting, but back up or commit existing changes first. Never reset/stash away active work.
2. Confirm `git --version`, `py -3 --version`, and `claude --version` in Windows Terminal. Install any missing CLI from its official provider instructions, under your own subscription. No API token is hard-coded here.
3. In a terminal at the G-PROJECT repository root, run:

```powershell
py -3 -m unittest discover -s Tools/AIDevTeam/tests -v
py -3 Tools/AIDevTeam/memory_check.py
py -3 Tools/AIDevTeam/pulse.py --dry-run
```

4. Start Claude Code **from that repository root** and run:

```text
/ship Add one small automated regression check for an existing dashboard helper
```

This invokes the planner -> coder -> tester -> reviewer workflow. The coordinator checks each stage, writes `.pipeline/runs/<RUN_ID>/...`, stops on failures and provides a verdict. It does not autonomously deploy, publish or merge.

If Claude Code does not recognize the custom skill, check that the local repo contains `.claude/skills/ship/SKILL.md` and restart the CLI in the repo root.

## Windows + Unreal verification (only once verified paths are available)

```powershell
py -3 Tools/AIDevTeam/run_unreal_tests.py `
  --project "D:\ActualPath\ProjectName.uproject" `
  --editor "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" `
  --run-dir ".pipeline\runs\<RUN_ID>" `
  --filter "Actual.Existing.Automation.Test.Name"
```

Do **not** use illustrative paths as if discovered. Confirm local editor, project and actual test filter first. The helper returns a nonzero exit code unless an actual Unreal automation JSON report shows executed, successful tests with no skipped/failed tests. Screenshots, reference comparison and owner sign-off remain mandatory for visually meaningful work.

## Handoff contract

Each run owns an isolated folder (ignored by Git):
- `request.md`: original bounded request.
- `spec.md`: `OPEN_QUESTIONS: NONE`, `UNREAL_REQUIRED: YES|NO`, `VISUAL_REQUIRED: YES|NO`.
- `changes.md`: actual file changes / implementation status.
- `test-results.md`: real test commands, count and existing log.
- `unreal-summary.json` + `unreal-report/index.json`: required for real Unreal edits.
- `evidence.md`, `evidence/before.png`, `evidence/after.png`: required for visual work, with reference and camera angles.
- `review.md`: final read-only reviewer verdict, captured by coordinator.

Gates must fail closed if any required file, test, source location, image, or approval is missing. A result of `READY_FOR_OWNER_REVIEW` does **not** mean merged or approved.

## First safe proof

Build one change to a **text-only** part of the existing Tree Production Dashboard (e.g. improve a unit-tested manifest validator), with zero game asset writes. Ensure unit tests pass, then separately validate any real browser or Unreal visual changes with before/after screenshots.

## MAPS safety roadmap

1. **Memory** (this branch): signposts across already-known project documentation; same data never needs to be copied into a dashboard.
2. **Agent** (this branch): four role-defined Claude Code agents, evidence gates and local command.
3. **Pulse** (this branch, *manual-only*): cap and record a deterministic read-only map audit. Later scheduling must be explicitly enabled and verify machine access, permissions and subscription terms.
4. **Screen** (later): read-only local dashboard bound to loopback or private network, serving existing JSONL records. No dashboard-owned state or paid UI dependencies.
5. **Optional always-on machine** (not installed): private network + least-privilege account + restricted tools; no public server, blanket machine permissions, or unsupervised send/delete/push.

Reference links: https://youtu.be/gsH0_0gB4IY and https://youtu.be/Zs3faMCDYNs . These establish the goals; successful local running and any specific feature behavior require testing.
