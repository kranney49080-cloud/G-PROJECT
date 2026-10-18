# HANDOFF TO CLAUDE CODE - Agentic 3D (A3D)

Written 2026-10-17 by Claude (cowork/cloud session) for Claude Code running on the owner's PC.
Read this file completely before touching anything. It is the single source of truth for "what is going on". Facts are tagged **[verified]** (seen in code, logs or game scripts), **[reported]** (the owner or a tool told us) or **[unverified]** (design intent or guess, test before relying on it).

---------------------------------------------------------------------
## 0. Ten-second summary

Agentic 3D is a system where real AI work shows up as Sims 4 characters doing things on screen.
- **The brain** = a Python orchestrator (`scripts/ai_os.py`) that routes tasks to model tiers and writes status JSON.
- **The Screen** = a Sims 4 script mod (`GProjectBridge.ts4script`, Python 3.7 inside the game) that reads that JSON and makes Sims act.
- **The factory** = Actionforge (actionforge.dev), a graph-based CI/CD system; its run events drive in-game visuals.
- Every Sim is named after the real AI/agent/tool/skill it stands for. No invented names, ever. At most 8 Sims on the lot.

What the owner wants to see (standing asks):
1. When the owner uses ChatGPT (phone app / voice), the **ChatGPT Sim looks at a phone**. Same for Gemini.
2. When **Codex** is working, the **Codex Sim types** at a computer. A combined phone+typing animation would be a bonus.
3. Every Sim has a status outline: **idle = no outline; doing something = colored outline** (blue working, green completed, red failed).
4. Actionforge pipelines/runs trigger visuals in the game (the factory).

The owner is non-programmer-level on tooling but very opinionated and fast. Read section 9 (how to work with them) before your first reply.

---------------------------------------------------------------------
## 1. Environment

| Thing | Value |
|---|---|
| PC | Windows 10, hostname `ranney-desktp`, user `kyler`, i5-10400F, 32 GB RAM, RTX 3060 12 GB **[reported]** |
| GPU rule | VRAM is reserved for Unreal Engine 5. Never load a model onto the GPU. CPU or off-machine only. |
| Brain/workspace root | `F:\MrMak\Workspace` (scripts in `F:\MrMak\Workspace\scripts\`, AI_OS in `F:\MrMak\Workspace\AI_OS\`) |
| Sims 4 install | `F:\The Sims 4`; build **1.121.361.1020** **[verified]** |
| Sims 4 user data | `C:\Users\kyler\OneDrive\Documents\Electronic Arts\The Sims 4\` (note OneDrive) |
| Live mod folder | `...\The Sims 4\Mods\GProject\` (contains `GProjectBridge.ts4script`, `GProjectSurvey.ts4script`, `bridge_config.json`, `gproject_bridge.log`, `gproject_survey.log`, `AI_Game_Dev_Studio\` packages, `presence_interactions.txt` after first lot load) |
| Sims 4 Studio | `F:\UNREAL GAME PROJECT FOLDER\Tools\THE SIMS 4 STUDIO` and `C:\Users\kyler\OneDrive\Documents\Sims 4 Studio` |
| Unreal projects | `F:\UNREAL GAME PROJECT FOLDER\` (separate project; not in this repo) |
| Actionforge CLI | `F:\Downloads\actrun-v0.16.11.cli-x64-windows\actrun.exe` (v0.16.11; SHA-256 recorded in `AI_OS/vendor/VENDOR_LOG.md`, not vendor-verified) |
| Drive sync | F: is synced to Google Drive by the desktop app. Hot IPC folders (`AI_OS\queue`, `AI_OS\state`) should be excluded from sync or they produce conflict copies like `sim_hud_status (1).json` that the poller never reads (blueprint section 4). |
| Other agents on this machine | Codex (state in `C:\Users\kyler\.codex`), Antigravity/Gemini ("Mr Mak Gemini", used as the **download assistant**), Claude desktop app, ChatGPT |

### Git situation - RECONCILE THIS FIRST
- GitHub: `https://github.com/kranney49080-cloud/G-PROJECT` (public; the repo name keeps the old "G-Project" name on purpose, do not rename).
- Remote branches **[verified 2026-10-17]**: `main`, `feature/maps-learning-agent-os-20261010`, `feature/claude-four-agent-unreal-pipeline`, and **`claude/sims4-bridge-20261012`** (the branch this handoff lives on).
- `claude/sims4-bridge-20261012` is branched from `main`, not from the feature branches. It contains a *copy* of the AI_OS source laid out as `AI_OS/...` plus `AI_OS/scripts/ai_os.py` (the PC has it at `F:\MrMak\Workspace\scripts\ai_os.py`, outside AI_OS).
- The blueprint says the PC worktree is on branch `feature/maps-learning-agent-os-20261010` with `git -c safe.directory="F:\MrMak\Workspace" status --short --branch`. **[reported]**
- **Do first:** on the PC, run `git status`, `git branch -a`, `git log --oneline -5` in `F:\MrMak\Workspace` and compare with the pushed branch. Decide with the owner how to merge: the PC worktree is the working truth (it has newer uncommitted edits possible). Never `git reset --hard` or force-push over the owner's work. Do not push to `main` without being asked; open a PR.
- The owner earlier said "dont worry about github" (do not nag about pushing). They then explicitly asked for a remote repo ("NOT LOCAL") and for this handoff. Pushing to `claude/*` branches is fine; anything touching `main` needs a yes.
- Repo is public: **never commit secrets** (see rules).

---------------------------------------------------------------------
## 2. Architecture

```
 owner / agents ──> queue/tasks/<id>.json ──> BRAIN (scripts/ai_os.py serve)
                                                 │  Tier 0..4 router (config/brain.json)
                                                 ▼
                                   state/sim_hud_status.json   (atomic writes)
 ChatGPT/Gemini listener ─> state/talk_state.json   {who:{active,since}}   (talk/talk_listener.py, mic_watcher.py)
 Codex activity watcher ──> state/talk_state.json   (talk/codex_watcher.py)
 Actionforge Orchestrator ─SSE─> talk/factory_bridge.py ─> state/factory_state.json
                                                 │
                       (all files under F:\MrMak\Workspace\AI_OS\state)
                                                 ▼
          SIMS 4 MOD  (Mods\GProject\GProjectBridge.ts4script, polls on game alarms)
            poller   -> HUD status       presence -> push phone/type interactions
            glow     -> colored outline  roster   -> rename household Sims
            ask_interaction/inject -> pie-menu "ask the brain" that writes tasks back to queue/
```
Principles **[from MASTER_BLUEPRINT.md]**: the Screen is a stateless, read-only dashboard (the only write-back is task files). Route by latency not cost ("is anything waiting on this result?"). All IPC writes are atomic (`temp + os.replace`). Success is written only after a result is retrieved and validated.

Model tiers (`AI_OS/config/brain.json`): tier0 deterministic Python, tier1 local CPU model (never GPU), tier2 fast cloud (default interactive; configured as Groq free tier, DeepSeek alt), tier3 heavy (Claude via OpenRouter configured; Agent SDK adapter still to write), tier4 batch (Gemini batch, overnight only). **The owner will not pay for Groq or other APIs** - free tiers only; do not add paid dependencies. Keys come only from environment variables (`GROQ_API_KEY`, `OPENROUTER_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`); `start_brain.bat` copies them from the Windows user environment into the process. No Suno API.

---------------------------------------------------------------------
## 3. Repository map (`AI_OS/`)

| Path | What it is |
|---|---|
| `MASTER_BLUEPRINT.md` | Authoritative architecture, data contracts, phasing, decision log. Read all of it. |
| `OFFICE_PLAN.md` | The 24x20 lot layout and which Sim sits where (zones/desks). |
| `NAMING_NOTE.md` | Why `gproject`/`GProject` identifiers remain internally while visible text says "Agentic 3D". |
| `config/staff.json` | **48** roster entries (sim_id, name, kind, role, dept, tier, skills). Names = real AIs/tools/skills. |
| `config/office.json` | Office zones/desks/waypoints (waypoint ids are filled in as desk object ids are captured in-game). |
| `config/brain.json`, `metrics.json` | Tier map; metrics. |
| `sims4_bridge/` | The in-game mod: `src/gproject_bridge/*.py`, `build_mod.py`, `build.bat`, `BUILD_SIMS_MOD.bat`, `deploy.bat`, `setup_py37.ps1`, `package/` (tuning XML + `make_pkg.py`), `config/bridge_config.json` (default). |
| `sims4_survey/` | Separate small survey mod that dumps lot objects (`state/lot_objects.json`) and logs; has `DEPLOY_RULES.md`. |
| `talk/` | Brain-side watchers and the Actionforge bridge (see section 6). |
| `scripts/ai_os.py` | The brain/orchestrator (copy; canonical copy at `F:\MrMak\Workspace\scripts\ai_os.py`). Many `.pre-*.bak` siblings exist on the PC, not in git. |
| `vendor/VENDOR_LOG.md` | Provenance/hash/licence log for third-party files. Big vendor files are NOT in git (`.gitignore`). |
| `state/`, `logs/`, `backups/`, `queue/` | Runtime, gitignored. `backups/` holds a 11 MB Sims save backup (`Slot_00000002.save.before-funds`). |

Not in git but important on the PC: `AI_OS\sims4_bridge\tools\py37\` (embedded Python 3.7.0), `AI_OS\vendor\decompiled_game\decompiled_game.zip` (3,256 decompiled game .py files, ~8 MB, user must extract), `AI_OS\vendor\{s4cl,lot51,bluuberry,s4pe,script_reloader,decompiler}`.

---------------------------------------------------------------------
## 4. The Sims 4 mod in detail

### 4.1 Build and deploy
- A `.ts4script` is a zip of **Python 3.7 `.pyc`** files (magic `420d0d0a`, 3394). It MUST be compiled with Python 3.7; the build script refuses anything else.
- Build: `AI_OS\sims4_bridge\BUILD_SIMS_MOD.bat` - build only, logs to `build_log.txt`, pauses so the window stays open. Output `dist\GProjectBridge.ts4script` (currently 34,486 bytes, **17 modules**). Last good build: `EXIT CODE: 0`.
- `deploy.bat` builds AND copies into the Mods folder (overwrites the installed script). **Never run it, and never overwrite the installed file, without the owner's explicit OK.** The installed copy was replaced on 2026-10-16 with owner approval; the previous 13-module version is saved beside it as `GProjectBridge.ts4script.old-before-presence`.
- The cloud sandbox had no Python 3.7. When editing from a machine without it, validate with `ast.parse(src, feature_version=(3,7))` and fake-module simulation tests, then build on the PC. You (on the PC) can build directly with `tools\py37\python.exe build_mod.py <project_dir>`.
- Game must be restarted to load a new script; "Script Mods Allowed" must be on in Game Options -> Other. Errors land in `...\The Sims 4\lastException*.txt` and `Mods\GProject\gproject_bridge.log`.
- `.bat` files must have **CRLF** line endings or cmd mangles them.

### 4.2 Modules (`src/gproject_bridge/`)
| Module | Role |
|---|---|
| `bootstrap.py`, `__init__.py` | Entry; installs hooks on import. |
| `hooks.py` | Wraps `zone.Zone.on_loading_screen_animation_finished`; after the original runs it starts, each in its own try/except: `brainlaunch.ensure_running()`, `poller.start()`, `presence.start()`, `glow.start()`. |
| `config.py`, `paths.py`, `log.py` | Loads `Mods\GProject\bridge_config.json`; paths; logging to `gproject_bridge.log`. `bridge_config.json` today: `state_dir`, `queue_tasks_dir`, `status_file`, `poll_seconds` (3), `sim_map` (0413-0416 -> Sim ids). Optional keys `presence`, `glow`, `roster` override module defaults. |
| `poller.py` | Alarm-driven read of `sim_hud_status.json`; `poller.current` holds the latest entry (sim_id, status, role, ...). |
| `notifier.py` | In-game notifications for HUD changes. |
| `taskqueue.py`, `ask_interaction.py`, `inject.py` | Pie-menu "ask the brain": injects interactions onto Sims; writes task JSON files to `queue/tasks/`. Tuning names `GProject_AskBrain` etc. (see NAMING_NOTE). |
| `brainlaunch.py` | Starts the brain if not running (uses `state/brain.alive`). Never kill/restart the brain without permission. |
| `survey.py` | Dumps lot objects (auto "simoff" hook installed 2026-10-14 22:07 - verification still open). |
| **`presence.py`** | **Phone/typing.** Reads `talk_state.json` (`{who:{active,since}}`, keys chatgpt/gemini/codex) and `factory_state.json`. For each active actor pushes a game interaction onto the Sim of that name via `sim.push_super_affordance(aff, target, InteractionContext(sim, SOURCE_SCRIPT, Priority.High))`; cancels via `find_interaction_by_affordance(aff).cancel(FinishingType.USER_CANCEL, ...)` when inactive. Retries every 12 s, gives up after 5 failures (toggle to retry). **`interactions` config is EMPTY** (`{"phone":[],"type":[]}`) so it logs "no interaction configured" until names are supplied. `discover()` writes `Mods\GProject\presence_interactions.txt` on every lot load listing interaction tuning names containing phone/computer/laptop/typing/tablet/cell/texting/text_. Targets: phone -> the Sim itself, type -> nearest object offering the interaction. Factory option: a configured Sim types while any Actionforge run is `running`. |
| **`glow.py`** | **Status outline.** Uses the game's own call-to-action highlight: `Distributor.instance().add_op(sim, distributor.ops.SetCallToAction(color, speed, thickness))`; off = `SetCallToAction(0,0,0)`. Styles: working `[0xFF2D8CFF, 1.0, 0.004]` blue, completed `[0xFF2ECC40, 0.2, 0.004]` green (auto-off after 30 s), failed `[0xFFFF3B30, 3.0, 0.005]` red fast, idle = none. Status sources, strongest first: `gp.glow test` overrides -> HUD file (sim_id -> name through staff.json) -> presence actors "working". The game's own tuning uses thickness 0.001-0.005; **larger values are untested** (the owner wants it bigger - `gp.glow size <n>` exists to experiment). How it coexists with the selection ring is untested. |
| **`roster.py`** | Renames existing household Sims to the on-duty AI names (default Claude, Codex, ChatGPT, Gemini, Antigravity, Planner, Coder, Tester; max 8). Only renames - never creates/moves/deletes Sims. Originals saved to `Mods\GProject\roster_backup.json`; `gp.roster undo` restores. **The household needs enough Sims**; creating Sims by script is not implemented. |
| `cmds.py` | Cheat commands (see 4.3). |

### 4.3 In-game commands (open the cheat console with Ctrl+Shift+C)
`gp.status`, `gp.task <words>`, `gp.dump`, `gp.presence [test <who> on|off|clear]`, `gp.interactions`, `gp.roster [apply|undo]` (no arg = dry run), `gp.glow [test <name> <working|completed|failed|off|clear> | size <n> | off]`.

### 4.4 Game API facts verified from decompiled game scripts (build 1.121.361.1020)
- `Sim.push_super_affordance(affordance, target, context)`; `InteractionContext(sim, InteractionContext.SOURCE_SCRIPT, Priority.High)` (`interactions.context`, `interactions.priority`).
- Cancel: `sim.find_interaction_by_affordance(aff).cancel(FinishingType.USER_CANCEL, cancel_reason_msg=...)` (`interactions.interaction_finisher`).
- Interaction tuning classes: `services.get_instance_manager(sims4.resources.Types.INTERACTION).types` (dict; name via `__name__`).
- `services.sim_info_manager().instanced_sims_gen()`, `services.object_manager().valid_objects()`, `obj.super_affordances()`, `services.active_household().sim_info_gen()`; `SimInfo.first_name/last_name` have setters.
- Timers: `alarms.add_alarm_real_time(owner, clock.interval_in_real_seconds(n), cb, repeating=False)` (re-arm each tick; keep the owner object alive at module level or the weak ref dies).
- Commands: `sims4.commands.Command("gp.x", command_type=CommandType.Live)`.

### 4.5 Game data you cannot easily see
Interaction **tuning is not in the Python zips** and was not found in SimulationFullBuild0/DeltaBuild0/Preload packages (animation/object binary data), Sims 4 Studio's sqlite (numeric ids only), or any exported XML. Everything-search found nothing. A DBPF2 parser was written for exploration (sandbox only). This is why the phone/computer interaction names are unknown.

---------------------------------------------------------------------
## 5. Roster and naming rules
- Each AI/agent/tool/skill = one Sim, named exactly after the real thing (Claude, Codex, ChatGPT, Gemini, Antigravity, Planner, Coder, Tester, Reviewer, GitHub, FFmpeg, ...). `staff.json` is the list (48). The owner corrected earlier mentions of 38: it is 48.
- At most 8 on the lot at once (those on a task); the rest "work remotely".
- Rules baked into `OFFICE_PLAN.md`: the Animation & Physics room is Claude-only; Codex is owner-approval-only, never auto-assigned; Meshy has no API key; PinWright production routing is blocked until `.uproject` and connection agree.
- Visible text says **Agentic 3D** (or A3D). Never write "G-Project" where the owner will read it. Internal identifiers (`gproject_bridge`, `GProject_*` tunings, `Mods\GProject`, `gp.*`, the GitHub repo name) stay.

---------------------------------------------------------------------
## 6. Actionforge (the factory)
- Graph-based CI/CD. Orchestrator `https://orch.actionforge.dev`. CLI `actrun`. REST API v2 + SSE streams: `/api/v2/ci/runs/stream`, `/api/v2/ci/agents/stream`, `/api/v2/ci/queue/stream`. Python `urllib` needs a browser-like `User-Agent` or requests are blocked **[verified]**.
- Three keys (names only; values live in the owner's environment, never in files or chat): **KEY1** read-only PAT (used by `factory_bridge.py`), **KEY2** agent token (runner: `actrun agent --token ...`), **KEY3** admin PAT. Launchers: `talk\KEY1_READONLY_bridge.bat`, `KEY2_AGENT_runner.bat`, `KEY3_ADMIN_check.bat`. The token is read from env `ACTIONFORGE_TOKEN` or typed at a prompt; never persisted. Earlier in the project some tokens were pasted into chat by mistake; the owner was told to delete them and issue fresh ones - **confirm that happened**, and never repeat or store a token you see.
- Agent registered: `kranney49080-cloud-agent`. A test pipeline `build-pong-game.act` ran: run `6ad1b0aaa0a4ac934241539b` finished `success`, queue 0.
- `talk/factory_bridge.py` subscribes to the three streams and writes `state/factory_state.json` (`{updated, connected, runs, agents, queue}`). Agents event shape is verified (`{id,name,labels,status,registered_at,owner_user_id}`); **run field names are still unverified.** The bridge was patched to log the first 30 raw run events as `{"kind":"runs_live"}` lines in `state/factory_raw_sample.jsonl` and to try more field-name variants for agent/project (`agent`, `agent_name`, `runner`, `repo`, `project`, ...). The *running* bridge process is still the old code until the owner restarts `KEY1_READONLY_bridge.bat`. Backup: `factory_bridge.before_raw_log.py`.
- Before using any MCP/agent token features, read Actionforge's "Agents" and "Agentic Coding" docs pages (not yet read).
- Two Claude docs exist (claude.ai artifacts): a compact master document "Actionforge in Agentic 3D" (done; one open comment on whether to keep it separate from or merge it into the master plan), and the big master plan `https://claude.ai/artifact/BVM28cRBJuRaE6TRHr2A5e`.

Other watchers (`talk/`): `talk_listener.py` writes `state/talk_state.json` (WHO = gemini/chatgpt); `mic_watcher.py` (mic activity) and `codex_watcher.py` (Codex activity) feed it; `discover_*.bat` are calibration helpers; `TEST_hello_world.bat` runs the hello-world pipeline. `state/talk_state.json` did not exist yet at handoff - the Codex watcher calibration and mic discovery are still open.

---------------------------------------------------------------------
## 7. Current state (2026-10-17)

DONE
- Blueprint, naming, office plan, roster (48), tier config.
- Mod: poller/notifier/ask-brain, presence, roster, glow all written, syntax-checked for 3.7, simulation-tested, built (17 modules) and **installed 2026-10-16** (owner OK). Backup of previous build beside it.
- Game scripts decompiled (decompyle3) to `vendor\decompiled_game\decompiled_game.zip`. Failed to decompile: `si_state`, `constraints`, `interaction_picker`, `base_interactions`, `animal_tests`, `sims4/log` (see `decompile_errors.txt`).
- Actionforge connected, agent registered, one pipeline run succeeded.
- GitHub branch pushed with all source + this handoff.

NOT YET DONE / UNTESTED
- **Nothing has been tested in the running game.** First job after the owner loads a lot: check `Mods\GProject\gproject_bridge.log` for `presence: started` and `glow: started`; run `gp.glow test Claude working`.
- `presence.interactions` is empty -> no Sim can phone/type yet.
- Outline: is thickness > 0.005 honoured? Does it stack with the selection ring? Unknown.
- The Sims named ChatGPT/Codex/Gemini must exist in the active household; `gp.roster apply` only renames.
- `factory_state.json` run fields; per-pipeline -> Sim mapping (offered, owner has not said yes).
- Codex watcher calibration; mic discovery; iPhone Shortcuts (owner's job); auto-simoff verification.

PARKED BY OWNER - DO NOT RESUME UNTIL TOLD
- The hunt for the game's phone/computer interaction tuning names. Quote: "dont focus on this until i tell you too." Two approaches were prepared: (A) in-game console `interactions.push` experiments; (B) Sims 4 Studio's tuning browser. When un-parked, begin from `presence_interactions.txt`.

---------------------------------------------------------------------
## 8. Prioritised backlog (suggested order, confirm with owner)

1. **Reconcile git** (section 1) and run `BUILD_SIMS_MOD.bat` on the PC to prove the repo builds clean. Acceptance: `EXIT CODE: 0`, 17 modules, identical module list to the installed file.
2. **In-game smoke test** with the owner present: lot loaded, log lines present, `gp.glow test <name> working|completed|failed|off`, `gp.roster` dry run. Record exact results in the log; do not "fix" unseen failures by guessing.
3. **Outline size/visibility experiments** (`gp.glow size 0.006 / 0.01 / 0.02`) and coexistence with the selection ring; document the maximum that renders.
4. **Restart the factory bridge (ask first)**, run an Actionforge job, read `factory_raw_sample.jsonl` (`runs_live`), fix agent/project/status field mapping in `factory_bridge.py` and `presence._desired` (it currently expects `runs[*].status == "running"`), then map pipelines -> Sims if the owner agrees.
5. **Un-park the interaction hunt only when told**, then fill `presence.interactions` in `bridge_config.json`, test phone and type on the ChatGPT/Codex Sims, then the combined phone+type bonus.
6. Create-Sim support (spawn missing household members) or document a "household must contain N Sims" setup step.
7. Brain: the Claude Agent SDK adapter for tier 3 (blueprint wants structured responses, not CLI stdout parsing); `watchdog`-based persistent service registered in Task Scheduler (blueprint Phase 2).
8. Hardening: move `queue/` and `state/` out of Drive sync; add tests that run under plain Python 3.7 with fake game modules (the simulation tests used during development were not committed - recreate them in `AI_OS/sims4_bridge/tests/`).
9. Housekeeping: confirm exposed tokens were revoked; resolve the docs comment (separate vs merged master plan); open decisions listed in the master plan.

---------------------------------------------------------------------
## 9. Rules of engagement (the owner's standing instructions - obey literally)

**Safety / ownership**
- No secrets in files, commits, logs or chat. Env vars only. If you see a token, do not repeat it.
- Never overwrite the installed mod, run `deploy.bat`, restart/close the brain, close an app, or close any agent session without explicit permission. Preserve originals; work on copies; **ask before replacing established systems** (the backup-then-replace pattern with `.old-before-*` names is accepted).
- No permanent deletes. No account creation. Downloads need permission stating filename, source and size; the owner uses **Gemini/Antigravity as the download assistant** (write it a brief; it fetches into the right F: folder and logs hashes in `vendor/VENDOR_LOG.md`).
- Do not touch the Claude app's permission mode; only the owner flips it.
- New folders go on **F:**. The RTX 3060 is for Unreal only. No paid APIs; no Suno API.

**Process**
- **Two-failure rule:** after two failures, stop, record the exact errors, and ask before resuming. Do not retry unchanged code. (Example: pip failed twice on `spark-parser` -> stopped -> Gemini fetched wheels.)
- Do things yourself with your tools; don't hand the owner manual steps you can do. When you truly need them to run something, **name exactly ONE file with its full path as a clickable link**. They were furious about "a dozen .bats" and windows that closed before they could read output: launchers must `pause` and log to a file.
- Whenever you mention a file or folder, give the **full path** (and a link where the client supports it).
- Verify, don't claim: after writing a file, check size/mtime on disk (the cloud bridge once re-sent stale staged copies; see `sims4_survey/DEPLOY_RULES.md`).
- Keep messages short and concrete. They type in capitals when frustrated; that is a signal you made them repeat themselves or hid a result. Lead with the result, then the one next step.
- "Don't worry about the lights" (ignore lighting concerns in the Sims lot).
- Confirm the current work budget/checkpoint before a substantial implementation cycle.

---------------------------------------------------------------------
## 10. Gotchas that already cost time
- Python 3.7 only inside the game; no f-string `=`, no walrus, no `typing` features newer than 3.7, no positional-only params.
- Re-arm alarms after every tick; keep alarm owners as module globals.
- Every hook/tick body must catch all exceptions - an uncaught error in a game callback can break the zone. Log, don't raise.
- A zone reload calls `on_loading_screen_animation_finished` again: `start()` functions must be idempotent (they are; keep them so).
- Interaction names are class `__name__`s of loaded tuning; IDs are hashes of the names, so renaming tunings breaks things (NAMING_NOTE).
- `State` files must be written atomically; the poller must never see half a file.
- Windows `.bat`: CRLF, `setlocal enabledelayedexpansion` + `!errorlevel!` for exit codes inside blocks.
- Python `urllib` to Actionforge needs a browser User-Agent.
- Computer-use quirks (if you drive the desktop): pressing Enter on a selected search result opens an "Open with" dialog; Everything search was the fast way to find files.

---------------------------------------------------------------------
## 11. Your first 30 minutes
1. Read: this file, `MASTER_BLUEPRINT.md`, `OFFICE_PLAN.md`, `NAMING_NOTE.md`, `sims4_bridge/README.md`, `sims4_survey/DEPLOY_RULES.md`.
2. `git` reconciliation (section 1) - read-only commands only until the owner approves a plan.
3. Compare the installed script with the repo build: list `Mods\GProject\` and confirm `GProjectBridge.ts4script` is 34,486 bytes with 17 modules; confirm the `.old-before-presence` backup exists.
4. Run `BUILD_SIMS_MOD.bat`'s Python command yourself (`tools\py37\python.exe build_mod.py AI_OS\sims4_bridge`) into a scratch copy, not over `dist\` unless asked; report module count.
5. Read `Mods\GProject\gproject_bridge.log` tail and `presence_interactions.txt` if present.
6. Reply to the owner with: what you found, the git plan, and the single next action you need from them (usually "load the lot in-game").
