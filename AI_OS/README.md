# G-PROJECT agent OS — starter implementation

Design references:
- Ray Fu's four specialist agents: https://www.raycfu.com/guides/four-agent-dev-team
- Pav's MAPS memory map and read-only display approach: https://github.com/pavrus117/ai-os-maps-guide
- Claude Code skill specification: https://code.claude.com/docs/en/skills
- Skill engineering reference, YouTube: https://www.youtube.com/shorts/mpobP7xQ-oQ

This is a practical **M (Memory) + A (Agent)** foundation, NOT a continuously running autonomous system. P (Pulse) is a disabled registry; S (Screen) is deferred. External videos' full spoken instructions were not independently recovered. The above source documents and their design patterns informed this implementation; no paid dashboards were downloaded.

## Activation on a Windows G-PROJECT checkout

1. Check out the feature branch or merge its reviewed PR into a working repo. Keep unrelated Unreal assets unchanged.
2. Install official Claude Code and Python 3.10 or newer. Use your own supported account sign-in. No additional paid agent harness is required by these files.
3. In Windows Terminal at repository root, run:
   - python scripts/ai_os.py check
   - python -m unittest discover -s tests -v
   - python scripts/ai_os.py route "harvest Mifune sword animation with sound"
   - python scripts/ai_os.py recall "Mifune retarget"
4. Open Claude Code in the same repo. Try /ship followed by a SMALL self-contained feature request. The four agents have their own context and handoffs under .pipeline/.
5. For any Unreal work, run /unreal-verify and submit actual editor images, sound and PIE test evidence before accepting.
6. On an error, run /learn. A deterministic fallback is:
   python scripts/ai_os.py learn --task "Mifune retarget" --symptom "feet slide" --cause "incorrect root transform" --remedy "align root in retarget profile" --proof "PIE screenshot and captured clip" --skill animation-harvest
   (Example only: replace with evidence of an actual occurrence.)

Skill selection: the descriptions in each .claude/skills/*/SKILL.md allow automatic context-sensitive loading. The deterministic route command provides a predictable fallback and records no data. The /skill-factory process uses six principles: start from a good example, one job/one trigger, set freedom level, verify, benchmark model choices, and improve from feedback.

Private storage: .ai-os-data/ and .pipeline/ are ignored by Git. In particular, *do not push raw memory logs* to this public repository. Never grant universal or administrator terminal permissions. Claude Code will not run from this GitHub commit alone; it has to be launched on an authorized machine.

## Next milestones
- Gate 1: map, router and unit tests pass.
- Gate 2: live Claude Code discovers skills and /ship runs with independent review.
- Gate 3: real Unreal PIE plus screenshot and audio verification of one bounded change.
- Gate 4: replay past failure examples, collect reviewer-approved skill improvements.
- Gate 5: owner-approved private machine scheduler with budgets, then read-only dashboard.

Owner alone marks acceptance. Independent review does not mean automatic deployment.

