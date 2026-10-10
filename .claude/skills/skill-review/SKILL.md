---
name: skill-review
description: Review exactly one proposed G-PROJECT Claude Code skill against golden outputs, one-job trigger, safety boundaries, and verification evidence.
disable-model-invocation: true
---

One skill file path: $ARGUMENTS

1. Read Tools/AIDevTeam/skills-standards.md and the skill supplied as the single argument.
2. Do not create or edit production files. Reject path traversal, missing skill files or multiple supplied skills.
3. Inspect skill metadata: unique name, one specific trigger, clear handoff/output, and when to stop. Ensure scope is bounded, permissions explicit, references real and exact, and model cost not assumed.
4. Find one documented good-output example, one failure case and an independently executable test for objective rules. If missing, mark the skill NEEDS_WORK.
5. If a skill touches Unreal or visuals, insist on a real automation report or before/after screenshots from an actual run; no screenshots means no approval.
6. Respond with exactly STATUS: READY_FOR_OWNER_REVIEW, NEEDS_WORK or BLOCK; then EVIDENCE: with grounded file paths; then RECOMMENDED_CHANGES: with concrete next edits. Do not auto-edit the skill based on untested suggestions.
