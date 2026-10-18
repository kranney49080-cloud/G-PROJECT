# Agentic 3D (A3D) - Claude Code handoff

Owner: kranney49080 (Windows PC "ranney-desktp"). Start here, then read `AI_OS/MASTER_BLUEPRINT.md`, `AI_OS/OFFICE_PLAN.md`, `AI_OS/NAMING_NOTE.md`.

## What this is
A Sims 4 bridge mod ("the Screen") for a Python AI orchestrator ("the brain"). Real-world AI activity shows up as Sims behaviour: ChatGPT/Gemini Sims on the phone, the Codex Sim typing, colored outline per status, Actionforge (actionforge.dev) as the software factory that drives in-game visuals. Every Sim is named after the real AI/agent/tool it stands for (no invented names). `AI_OS/config/staff.json` lists the roster; at most 8 on the lot. Do not write "G-Project" in anything visible; internal names (`gproject_bridge`, `gp.*` commands, the repo name) stay.

## Layout (all under `AI_OS/`)
- `sims4_bridge/src/gproject_bridge/` - the in-game mod (Python 3.7, game-embedded). Modules: presence (phone/type interactions), glow (status outline via SetCallToAction), roster (rename household Sims), poller (HUD file), cmds (`gp.*` cheats), survey, taskqueue, hooks, config.
- `sims4_bridge/BUILD_SIMS_MOD.bat` - build only (writes `dist/GProjectBridge.ts4script`, log `build_log.txt`). Uses embedded Python 3.7 at `sims4_bridge/tools/py37/` (not in git; run `setup_py37.ps1`).
- `sims4_survey/` - separate survey mod.
- `talk/` - brain-side watchers and the Actionforge bridge (`factory_bridge.py`, `codex_watcher.py`, `talk_listener.py`, `mic_watcher.py`).
- `scripts/ai_os.py` - the orchestrator ("brain"). `config/` - staff, office, brain settings.
- Runtime state (`state/`, `logs/`, `backups/`, `queue/`) is gitignored.

## Hard rules from the owner
- Never put API keys/tokens/passwords in files, commits or chat. Three Actionforge keys (read-only, agent, admin) live in the owner's environment only.
- Never overwrite the installed mod (`...\Documents\Electronic Arts\The Sims 4\Mods\GProject\GProjectBridge.ts4script`) or run `deploy.bat` without the owner's explicit OK. Back up the old file first (done once: `GProjectBridge.ts4script.old-before-presence`).
- Never restart or close the brain or any agent session without permission.
- Preserve originals, work on copies, ask before replacing established systems. New folders go on F:.
- Two-failure rule: after two failures stop, record the exact errors, ask before resuming.
- No paid APIs (no Groq etc.); the RTX 3060 VRAM is reserved for Unreal. No Suno API.
- Whenever you mention a file or folder to the owner, give the full path as a clickable link. When asking them to run something, name exactly ONE file; launchers must stay open and log (they said "it closes before I can read it").
- `.bat` files must have CRLF line endings.

## Status (2026-10-17)
- Built and installed: 17-module mod (presence, roster, glow, ...). Not yet tested in the real game.
- Parked by owner: hunting the game's phone/computer interaction tuning names (`presence.interactions` in `bridge_config.json` is empty until found). Start from `Mods\GProject\presence_interactions.txt` written on lot load. Don't resume until the owner says.
- Pending: restart `talk\KEY1_READONLY_bridge.bat` so `factory_bridge.py` logs raw runs; then read `state\factory_raw_sample.jsonl` to fix agent/project fields and map pipelines to Sims. Codex watcher calibration and mic discovery still open.
- Game facts (build 1.121.361.1020): scripts are Python 3.7 `.pyc` in a zip. Decompiled game scripts are in `AI_OS/vendor/decompiled_game/decompiled_game.zip` on the owner's PC (not in git). Verified APIs: `Sim.push_super_affordance`, `InteractionContext(sim, SOURCE_SCRIPT, Priority.High)`, `distributor.ops.SetCallToAction(color, speed, thickness)` (game tuning allows thickness 0.001-0.005).
