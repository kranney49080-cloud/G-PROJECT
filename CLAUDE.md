# G-PROJECT agent contract

G-PROJECT is a public coordination repository for an Unreal Engine project. The local Unreal project, machine, assets, and editor are NOT necessarily accessible.

For every implementation task:
1. Read AI_OS/MAP.md and the one relevant area signpost, then follow its primary source link. Do not replace project facts with copies in memory.
2. Read past failures using the /recall skill and use /skill-factory when a repeated failure or repeatable procedure needs a new skill.
3. Choose the narrowest suitable skill. Project skills are auto-discoverable by their YAML descriptions. Python routing is a deterministic check: python scripts/ai_os.py route "task".
4. For coding changes use /ship. Four independent roles: planner, coder, tester, reviewer. Every role passes a concrete handoff file under .pipeline/; no stale handoffs.
5. Use actual deterministic tests, plus in-editor Play-In-Editor, screenshots, video, sound validation when Unreal visual/animation behavior is involved. Source changes are NOT visual verification.
6. After mistakes, rework, regressions or durable successes use /learn to record an evidence-backed lesson. Suggest skill improvements but DO NOT silently mutate an accepted skill or delete history.
7. Never mark work owner-approved. The owner accepts completion after reviewing evidence.

Safety: no uncontrolled terminal elevation, automatic merging, destructive shell commands, public remote dashboard or unapproved sending/sharing/deletion. Branch per feature. Keep private lesson logs in gitignored .ai-os-data and never commit secrets or private files to this public repo.

Statuses are distinct: planned, implemented, tested, visually verified, owner-approved. Reference AI_OS/STATE.md for the current implementation limits.

