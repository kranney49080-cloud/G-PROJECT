# Agentic 3D (A3D) - Claude Code project memory

You are taking over a running project. **Read `AI_OS/HANDOFF.md` completely first** - it contains the architecture, environment, current state, backlog and the owner's rules. Then `AI_OS/MASTER_BLUEPRINT.md`, `AI_OS/OFFICE_PLAN.md`, `AI_OS/NAMING_NOTE.md`.

One-line version: a Sims 4 script mod ("the Screen", Python 3.7, `AI_OS/sims4_bridge`) mirrors real AI activity (ChatGPT/Gemini on phone, Codex typing, status outlines, Actionforge runs) from a Python orchestrator ("the brain", `AI_OS/scripts/ai_os.py`). Every Sim is named after the real AI/tool; max 8 on the lot. Say "Agentic 3D", never "G-Project", in anything the owner reads (internal identifiers keep the old name).

## Non-negotiables (full list in HANDOFF section 9)
- No keys/tokens/passwords in files, commits, logs or chat. Env vars only. Repo is public.
- Never overwrite the installed mod, run `deploy.bat`, or restart/close the brain or any app/agent without the owner's explicit OK. Preserve originals, work on copies, ask before replacing established systems.
- Two-failure rule: after two failures stop, record exact errors, ask before resuming.
- No paid APIs, no Suno API, GPU is reserved for Unreal, new folders on F:.
- Ask the owner to run at most ONE named file, with a full-path link; launchers must pause and log. Always give full paths for files/folders you mention.
- Game scripts are Python 3.7 only; `.bat` files need CRLF.
- Parked until the owner says otherwise: hunting the phone/computer interaction tuning names.
- Push only to `claude/*` branches; open a PR for `main`, never force-push, never reset the owner's worktree.

## Status pointer
Mod (17 modules incl. presence, roster, glow) is built and installed but untested in-game. Next step: git reconciliation, then an in-game smoke test with the owner. Details: HANDOFF sections 7 and 8.
