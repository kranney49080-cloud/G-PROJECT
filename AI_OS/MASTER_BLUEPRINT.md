# AGENTIC 3D: Master Architectural & Implementation Blueprint

**Document Purpose:** This is the authoritative reference document for the Agentic 3D. All AI agents (Claude, Gemini, Planner, Coder, Tester, Reviewer) MUST read and refer to this document before generating new architecture, modifying Unreal Engine C++ components, or altering the Python routing scripts.

**Last revised:** 2026-10-12 (see Decision Log, section 8)

**Deployment Environment:**
*   **Host Path:** F:\MrMak\Workspace
*   **Git Branch:** feature/maps-learning-agent-os-20261010
*   **Hardware:** i5-10400F (6c/12t, no AVX-512, no iGPU), 32GB RAM, RTX 3060 12GB, Windows 10
*   **Primary Objective:** Preserve local VRAM exclusively for Unreal Engine 5. No model is ever loaded onto the RTX 3060. Reasoning runs on CPU or off-machine.
*   **Current Topology:** Brain and Screen share one machine (`ranney-desktp`). A dedicated always-on brain host is planned but not provisioned; see section 4 for the portability rules that keep that migration a config change.
*   **The Screen:** The Sims 4 acts strictly as a stateless, read-only visual dashboard. It does not perform AI reasoning.

---

## 1. The MAPS Framework (Memory, Agents, Pools, Screen)
The MAPS directory structure decouples the visual interface from persistent project data.

**M - Memory (Local Append-Only):**
*   AI_OS/MASTER_BLUEPRINT.md: This file. The central architectural truth.
*   AI_OS/MAP.md: The domain signpost for the Python file-watcher.
*   AI_OS/config/brain.json: Tier-to-provider mapping (see section 3).
*   AI_OS/config/paths.json: The single location where host paths are defined.
*   AI_OS/queue/tasks/<task_id>.json: The intake queue. One file per task.
*   AI_OS/queue/processed/<task_id>.json: Completed tasks, moved here for idempotency.
*   AI_OS/state/sim_hud_status.json: Telemetry holding immediate cost metrics and active visual flags.
*   .ai-os-data/lessons.jsonl: The private, append-only ledger storing historical verification outcomes and C++ parameter tests.

**A - Agents (The Workforce):**
*   **Planner:** Decomposes prompts, bounds the Unreal Engine file scope, and establishes strict acceptance criteria.
*   **Coder:** The lead engineer modifying Unreal Engine C++ and Python scripts.
*   **Tester:** An independent verification agent that runs unit tests against the Coder's work.
*   **Reviewer:** A read-only gatekeeper checking regressions and evidence before owner sign-off.

**P - Pools (Skill Playbooks):**
*   Located in .claude/skills/<skill-name>/SKILL.md.
*   Active pools: ship, learn, recall, skill-factory, unreal-verify, animation-harvest.

**S - Screen (The Sims 4):**
*   A custom Python 3.7 script mod that uses the native alarms service to poll the memory folders and injects Pie Menus onto Sim objects to write back to the /queue/.

---

## 2. The JARVIS Topology & Latency-First Routing

**Routing principle: tier by latency, not by cost.** The question the Decider asks is *"is anything waiting on this result?"* — not *"how expensive is this task?"* Cost differences between tiers amount to a few dollars a month at this volume. Latency differences amount to hours. A HUD that reports yesterday's answer is indistinguishable from a broken one.

*   **Tier 0: Deterministic (No Model) — $0.00, instant**
    *   **Mechanism:** Plain Python. `subprocess.run(..., shell=False)` for OS actions.
    *   **Workload:** Routing by `sim_role`, status flag writes, waypoint selection, JSON schema validation, git status queries, clearing logs, launching URLs (e.g. ClickUp).
    *   **Rule:** A task must be *proven* to require inference before it is allowed to leave Tier 0. Every task kept here is one less source of latency and one less failure mode.

*   **Tier 1: Local CPU Model — $0.00, ~6-10 tok/s**
    *   **Mechanism:** llama.cpp or Ollama, **CPU only**. Phi-4 Mini 3.8B at Q4_K_M (~2.3GB) or Llama 3.2 3B (~2GB).
    *   **Workload:** Short classification, intent extraction, JSON shaping, and offline fallback when no network is available.
    *   **Constraints:** Run at low process priority pinned to no more than 2 cores — UE5 shader compilation saturates all 6. Budget 4GB system RAM, which is shared with UE5 and Sims 4. Published throughput figures of 10-15 tok/s come from 12-core CPUs with AVX-512; this host has neither, so expect the lower end. Never GPU-offloaded.

*   **Tier 2: Fast Cloud — $0.00 on free tier, sub-second (DEFAULT INTERACTIVE TIER)**
    *   **Mechanism:** Groq, OpenAI-compatible chat completions. Models: `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`.
    *   **Documented free-tier limits:** 30 req/min, 1,000 req/day, 8K tokens/min, 200K tokens/day.
    *   **Workload:** Any task with a Sim or a user waiting on the result. This is the default for interactive work.
    *   **Alternates:** Cerebras (same speed niche), DeepSeek, OpenRouter free models, or synchronous Gemini 3.1 Flash-Lite at $0.25/1M input.

*   **Tier 3: Heavy Reasoning — premium, seconds**
    *   **Mechanism:** Claude via the **Claude Agent SDK** (structured responses; do not shell out to the CLI and parse stdout). Gemini 3.1 Pro or 3.8 Flash as alternates.
    *   **Workload:** Complex Unreal Engine 5 C++ class generation, architectural refactoring, collision and physics algorithms, animation retargeting pipelines.

*   **Tier 4: Batch — 50% discount, up to 24h turnaround**
    *   **Mechanism:** Gemini 3.1 Flash-Lite via `client.batches.create()`. See scripts/batch_router_fixed.py.
    *   **Cost:** $0.125/1M input, $0.75/1M output.
    *   **Workload:** **Overnight bulk only.** Multi-file code reviews, documentation generation, large-scale validation sweeps.
    *   **PROHIBITED:** Any task with a Sim or user waiting. The Batch API targets 24-hour turnaround and jobs expire at 48 hours. It cannot drive a live HUD.

---

## 3. Brain Provider Abstraction

All model tiers are reached through a **single OpenAI-compatible chat-completions interface** in `scripts/brain/providers/`. Groq, DeepSeek, OpenRouter and local llama.cpp speak this natively; Gemini and Claude are reached through thin adapters implementing the same interface.

**Consequence:** switching or adding a brain is an edit to `AI_OS/config/brain.json`, never a rewrite of the router. The tier structure above is a default configuration, not a hardcoded dependency.

`AI_OS/config/brain.json` maps each tier to a provider, model id, and endpoint.

**Credential rule:** no API key is ever written to a tracked file, a config file, or a log. All keys are read from environment variables (`GEMINI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`). A provider whose key is absent is skipped with a logged warning, and the router falls through to the next available tier.

---

## 4. Host Portability (Single Machine Now, Dedicated Brain Host Later)

The brain currently runs on the same machine as the Screen. A dedicated always-on host is planned. These rules keep that migration a configuration change rather than a rewrite:

1.  **One transport module.** All queue and state access goes through `scripts/brain/transport.py`. Local filesystem today; an HTTP endpoint later. No other module touches `AI_OS/queue/` or `AI_OS/state/` paths directly.
2.  **No scattered host paths.** `F:\MrMak\Workspace` appears only in `AI_OS/config/paths.json`. Nothing else hardcodes it.
3.  **The Screen reads one configured location.** The Sims mod's polling target is defined in its own config, so repointing it at a network share or an HTTP endpoint is a one-line change.

**CONSTRAINT — Google Drive sync.** The F: drive is synced to Google Drive by the desktop app. `AI_OS/queue/` and `AI_OS/state/` are rewritten on every task and **must be excluded from sync**, or relocated to a local non-synced path. Sync churn adds latency to the HUD and can produce conflict copies (e.g. `sim_hud_status (1).json`) that the poller will never read. Durable project files on F: remain synced as normal; this applies only to the hot IPC path.

---

## 5. Data Contracts (Inter-Process Communication)
The Python backend and the game engine communicate strictly through these JSON schemas. AI agents generating updates MUST adhere to this formatting.

**A. Task Ingestion (AI_OS/queue/tasks/<task_id>.json)**
{
  "task_id": "T-001",
  "assigned_sim_id": "0413",
  "sim_role": "coder",
  "prompt": "String command from the user",
  "preferred_tier": "auto"
}

*   `"preferred_tier": "auto"` resolves on **whether anything is waiting on the result**, not on task size.
*   One file per task. The former single shared `task_in.json` is **deprecated**: it permitted only one in-flight task and raced with the Screen's poller.
*   On completion the file moves to `AI_OS/queue/processed/`. A task already present there is never re-run, so a restart mid-queue is safe.

**B. Telemetry & State Export (AI_OS/state/sim_hud_status.json)**
{
  "sim_id": "0413",
  "status": "COMPLETED",
  "assigned_role": "Reviewer",
  "task_description": "Summary of completed action",
  "error": null,
  "lifetime_stats": {
    "success_rate": 96.2,
    "batch_cost": 0.00012
  },
  "visual_cues": {
    "waypoint": 10583,
    "prop": "folder_01",
    "anim": "a_wave_friendly"
  }
}

*   **All writes MUST be atomic:** write to a temp file in the same directory, then `os.replace()`. The Screen polls on an alarm and must never observe a partially written file.
*   `status` may be `IDLE`, `WORKING`, `COMPLETED`, or `FAILED`. On `FAILED`, `error` carries a short human-readable reason so failures surface on the HUD instead of only in logs.
*   Success is only written after a result has been **retrieved and validated**. A terminal "succeeded" job state is not by itself evidence of a usable result.

---

## 6. Implementation Phasing & Rules of Engagement

**Phase 1: Environment & File Contracts**
*   Target directory is strictly F:\MrMak\Workspace.
*   Agents must verify the worktree using git -c safe.directory="F:\MrMak\Workspace" status --short --branch.

**Phase 2: The Orchestrator (scripts/ai_os.py)**
*   **Must run as a persistent service.** A `watchdog` observer on `AI_OS/queue/tasks/`, registered in Task Scheduler at logon. Dropping a task file is the only action required to trigger work. A hand-launched script is not an orchestrator.
*   Implements the Tier 0-4 Decider per section 2, through the provider interface in section 3.
*   Upon completion, write lessons to lessons.jsonl and update sim_hud_status.json atomically.

**Phase 3: The Sims 4 Bridge Mod (Screen)**
*   **CRITICAL:** Must be written and compiled in **Python 3.7.0**. The game engine will reject newer versions.
*   Must use the native game alarms.add_alarm() for polling. time.sleep() is forbidden.
*   **Alarm caveat:** in-game minutes scale with the game speed setting and stop entirely while paused, so a 5-in-game-minute interval freezes the HUD whenever the player pauses to build. Pin the poll to real time or shorten the interval substantially.
*   Requires Sims 4 Studio (S4S) to verify internal animation hashes.

**Phase 4: In-Game UI Injection**
*   Injects interaction IDs into Super Affordances to build the custom Pie Menu.
*   Utilizes ui_dialog_service to generate native center-screen pop-ups mapping the data from sim_hud_status.json.

**Phase 5: Verification Checkpoints**
1.  Run py -3 scripts\ai_os.py check to validate keyword routing.
2.  Run py -3 -m unittest discover -s tests -v for core logic checks.
3.  Ensure the private ledger .ai-os-data/lessons.jsonl is ignored by Git.

---

## 7. Rules of Engagement for Agents

*   **Two-failure rule:** after two consecutive failures, stop execution, record the exact errors, and ask before resuming. Do not retry unchanged code.
*   **Confirm budget** before beginning a substantial implementation cycle.
*   **Preserve originals.** Work on isolated copies. Ask before replacing an established system.
*   **Never write credentials** into tracked files, configs, or logs.

---

## 8. Decision Log

**2026-10-12 — Tier topology reorganized around latency.**
The original Tier 2 routed routine delegation to the Gemini Batch API for its 50% discount. Batch targets 24-hour turnaround and expires at 48, which is incompatible with a live HUD: a task triggered from the Sims pie menu would not report back until the next day. At flash-lite rates the discount is worth under $2/month at this project's volume, so latency wins. Batch was demoted to Tier 4 (overnight bulk only) and a free, sub-second cloud tier (Groq) became the default for interactive work. A deterministic Tier 0 and a zero-VRAM local CPU tier were added beneath it, on the principle that the cheapest and most reliable brain is no brain at all.

**2026-10-12 — Brain made pluggable.**
Providers are reached through one OpenAI-compatible interface so that changing brains is a config edit. Adopted because the host already runs several agent CLIs and the model landscape moves faster than this architecture should.

**2026-10-12 — Dedicated brain host deferred, portability rules adopted now.**
A second machine for the brain is wanted but not currently available. Rather than defer the design, section 4's transport and path rules were adopted immediately so the migration stays a config change.

End of Blueprint.
