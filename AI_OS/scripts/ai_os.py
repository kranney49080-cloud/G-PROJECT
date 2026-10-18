"""Agentic 3D orchestrator.

    py -3 scripts\\ai_os.py check                 routing table + config, no network
    py -3 scripts\\ai_os.py doctor                environment diagnostics
    py -3 scripts\\ai_os.py submit "do a thing"   enqueue a task
    py -3 scripts\\ai_os.py once                  drain the queue once, then exit
    py -3 scripts\\ai_os.py serve                 run as a service (Task Scheduler)

MASTER_BLUEPRINT.md sections 2-6. The orchestrator owns no model knowledge and
no path knowledge: tiers come from brain.json, paths from paths.py, and all
queue/state access goes through transport.py.
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))  # make `brain` importable

from brain import BrainConfig  # noqa: E402
from brain.paths import Paths  # noqa: E402
from brain.providers.base import BrainError  # noqa: E402
from brain import office, roster, tracking  # noqa: E402
from brain.router import BATCH_TIER, Router, describe_tiers  # noqa: E402
from brain.transport import LocalFileTransport, Task  # noqa: E402

POLL_SECONDS = 2.0
_stop = False

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# --------------------------------------------------------------------------
class Orchestrator:
    def __init__(self) -> None:
        self.paths = Paths.resolve().ensure()
        self.transport = LocalFileTransport(self.paths)
        try:
            self.config: BrainConfig | None = BrainConfig.load(self.paths.brain_config)
            tiers = set(self.config.tiers)
        except BrainError as e:
            _log(f"WARN brain config unavailable ({e}); Tier 0 only")
            self.config = None
            tiers = set()
        self.router = Router(self.paths, available_tiers=tiers)
        self.roster_dir = self.paths.ai_os / "roster"
        try:
            roster.ensure_seeded(self.roster_dir)
        except OSError as e:
            _log(f"WARN roster unavailable ({e})")

    def _record(self, task: Task, decision: Any, ok: bool, elapsed: float, error: str | None = None,
                output: str = "", usage: dict | None = None, cost: float = 0.0) -> None:
        """Update the Sim's stats. Never fails a task. Deterministic Tier 0 jobs are skipped."""
        if decision.is_deterministic:
            return
        try:
            extra = task.extra or {}
            sim = roster.record(
                self.roster_dir,
                sim_id=task.assigned_sim_id,
                task_id=task.task_id,
                prompt=task.prompt,
                ok=ok,
                elapsed_s=elapsed,
                error=error,
                skills=extra.get("skills"),
                difficulty=extra.get("difficulty"),
                collaborators=extra.get("collaborators") or (),
            )
            roster.credit_partners(
                self.roster_dir, task.assigned_sim_id,
                extra.get("collaborators") or (), ok,
            )
            tracking.append(self.roster_dir, tracking.measure(
                task=task, tier=decision.tier, ok=ok, elapsed_s=elapsed, output=output,
                error=error, usage=usage, sim=sim, cost_usd=cost,
            ))
        except Exception as e:  # stats are secondary to the task itself
            _log(f"WARN roster update failed ({e})")

    # -- one task --------------------------------------------------------
    def _wp(self, task: Task) -> int:
        """Waypoint of the desk this Sim should walk to for this task."""
        try:
            skills = (task.extra or {}).get("skills") or roster.tag_skills(task.prompt)
            return office.waypoint_for(self.paths.ai_os / "config", task.assigned_sim_id, skills)
        except Exception:
            return office.DEFAULT_WAYPOINT

    def _delegate(self, task: Task) -> None:
        """assigned_sim_id "auto": give the task to the best-suited Sim.

        Ranking is roster.suggest(): skill level + base aptitude - weakness
        penalty for the skills the prompt needs. An explicit Sim id is never
        overridden. Falls back to the default Sim if the roster is unreadable.
        """
        try:
            ranking = roster.suggest(self.roster_dir, task.prompt)
            best = ranking[0]
            sim = roster.load(self.roster_dir, best["sim_id"])
            task.assigned_sim_id = best["sim_id"]
            task.sim_role = sim.get("role", task.sim_role)
            board = ", ".join(f"{r['name']} {r['score']}" for r in ranking)
            _log(f"{task.task_id}: delegated to {best['name']} ({best['sim_id']}) "
                 f"for {best['tags'] or 'general'} [{board}]")
        except Exception as e:  # delegation must never fail a task
            task.assigned_sim_id = "0413"
            _log(f"WARN delegation failed ({e}); using 0413")

    def handle(self, task: Task) -> bool:
        if str(task.assigned_sim_id).strip().lower() in ("auto", "best"):
            self._delegate(task)
        decision = self.router.decide(task)
        _log(f"{task.task_id}: -> {decision.tier} ({decision.reason})")

        self.transport.write_state(
            status="WORKING",
            task_description=task.prompt[:160],
            sim_id=task.assigned_sim_id,
            assigned_role=task.sim_role.title(),
            waypoint=self._wp(task),
            prop="folder_01",
            anim="a_tradeshow_tablet_idle",
        )

        started = time.monotonic()
        cost = 0.0
        usage: dict[str, Any] = {}
        try:
            if decision.is_deterministic:
                output = self.router.execute_tier0(task, decision)
                model = "deterministic"
                if output.startswith("[FAIL]"):
                    raise BrainError(output[len("[FAIL] "):])
            elif decision.tier == BATCH_TIER:
                # Nothing has run yet, so this is NOT a completed task. Park it
                # for the overnight dispatcher and report it as still pending,
                # or the HUD would claim work that hasn't happened.
                dest = self.transport.defer_to_batch(task)
                waiting = len(self.transport.pending_batch())
                _log(f"{task.task_id}: deferred to batch queue ({waiting} waiting) -> {dest.name}")
                self.transport.write_state(
                    status="WORKING",
                    task_description=f"{task.task_id} queued for overnight batch ({waiting} waiting)",
                    sim_id=task.assigned_sim_id,
                    assigned_role=task.sim_role.title(),
                    waypoint=self._wp(task),
                    prop="folder_01",
                    anim="a_tradeshow_tablet_idle",
                )
                self.transport.append_lesson(
                    {
                        "task_id": task.task_id,
                        "tier": BATCH_TIER,
                        "ok": None,
                        "deferred": True,
                        "note": "awaiting overnight batch dispatch",
                        "prompt": task.prompt[:300],
                    }
                )
                return True  # correctly handled, but deliberately not a success
            else:
                if self.config is None:
                    raise BrainError(
                        "No brain config, so only Tier 0 tasks can run. "
                        f"Expected {self.paths.brain_config}"
                    )
                provider = self.config.build(decision.tier)
                result = provider.complete(task.prompt)
                output = result.text.strip()
                model = result.model
                usage = {"model": result.model, "input_tokens": result.input_tokens,
                         "output_tokens": result.output_tokens, "latency_s": result.latency_s}
                cost = result.cost_estimate(*self.config.pricing(decision.tier))
                _log(
                    f"{task.task_id}: {result.latency_s:.2f}s, "
                    f"in={result.input_tokens} out={result.output_tokens}, ${cost:.6f}"
                )
        except BrainError as e:
            elapsed = time.monotonic() - started
            _log(f"{task.task_id}: FAILED after {elapsed:.2f}s - {e}")
            self.transport.write_state(
                status="FAILED",
                task_description=task.prompt[:160],
                sim_id=task.assigned_sim_id,
                assigned_role=task.sim_role.title(),
                error=str(e)[:300],
                waypoint=self._wp(task),
                prop="none",
                anim="a_react_frustrated",
                succeeded=False,
            )
            self.transport.append_lesson(
                {
                    "task_id": task.task_id,
                    "tier": decision.tier,
                    "ok": False,
                    "error": str(e)[:500],
                    "elapsed_s": round(elapsed, 3),
                }
            )
            self._record(task, decision, False, elapsed, str(e), usage=usage)  # before finish(): needs the queue file
            self.transport.finish(task, ok=False)
            return False

        elapsed = time.monotonic() - started
        self.transport.write_state(
            status="COMPLETED",
            task_description=f"{task.task_id}: {output[:140]}",
            sim_id=task.assigned_sim_id,
            assigned_role=task.sim_role.title(),
            waypoint=self._wp(task),
            prop="folder_01",
            anim="a_wave_friendly",
            cost_delta=cost,
            succeeded=True,
        )
        self.transport.append_lesson(
            {
                "task_id": task.task_id,
                "tier": decision.tier,
                "model": model,
                "ok": True,
                "elapsed_s": round(elapsed, 3),
                "cost": round(cost, 8),
                "prompt": task.prompt[:300],
                "output": output[:1000],
            }
        )
        self._record(task, decision, True, elapsed, output=output, usage=usage, cost=cost)  # before finish(): needs the queue file
        self.transport.finish(task, ok=True)
        _log(f"{task.task_id}: done in {elapsed:.2f}s")
        return True

    def drain(self) -> tuple[int, int]:
        ok = fail = 0
        for task in self.transport.iter_claimed():
            if self.handle(task):
                ok += 1
            else:
                fail += 1
        return ok, fail


# --------------------------------------------------------------------------
def cmd_roster(args: argparse.Namespace) -> int:
    rdir = Paths.resolve().ai_os / "roster"
    roster.ensure_seeded(rdir)
    if args.what == "suggest":
        for row in roster.suggest(rdir, " ".join(args.rest)):
            print(f"{row['score']:>6}  {row['name']} ({row['sim_id']})  tags={row['tags']}")
        return 0
    ids = [args.what] if args.what else list(roster.SEEDS)
    for sid in ids:
        print(roster.card(roster.load(rdir, sid), "ansi"))
        print()
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    rdir = Paths.resolve().ai_os / "roster"
    ids = [args.sim] if args.sim else list(roster.SEEDS)
    for sid in ids:
        print(tracking.format_summary(roster.load(rdir, sid)["name"], tracking.summarize(rdir, sid)))
        print()
    return 0


def cmd_usage(_: argparse.Namespace) -> int:
    u = tracking.usage_today(Paths.resolve().ai_os / "roster")
    c = u["caps"]
    print(f"Today ({u['date']}), all Sims, free-tier model:")
    print(f"  requests {u['requests']} / {c['requests_per_day']} ({u['requests_pct_of_day']}%)")
    print(f"  tokens   {u['tokens']} / {c['tokens_per_day']} ({u['tokens_pct_of_day']}%)")
    print(f"  peak requests in one minute: {u['peak_requests_per_min']} (cap {c['requests_per_min']})")
    return 0


def cmd_rate(args: argparse.Namespace) -> int:
    rdir = Paths.resolve().ai_os / "roster"
    if not 1 <= args.stars <= 5:
        print("stars must be 1-5")
        return 2
    ok = tracking.record_external(rdir, args.task_id, "user_stars", args.stars, "user")
    print("saved" if ok else f"no tracked task {args.task_id}")
    return 0 if ok else 1


def cmd_check(_: argparse.Namespace) -> int:
    paths = Paths.resolve()
    print(f"workspace : {paths.root}")
    print(f"queue     : {paths.tasks_dir}")
    print(f"state     : {paths.hud_state}")
    print(f"ledger    : {paths.lessons}")
    try:
        cfg = BrainConfig.load(paths.brain_config)
        print(f"config    : {cfg.source}")
        print(f"tiers     : {', '.join(cfg.tiers)}  (default: {cfg.default_tier})")
        print(f"fallback  : {' -> '.join(cfg.fallback_order)}")
    except BrainError as e:
        print(f"config    : UNAVAILABLE - {e}")

    tiers = describe_tiers()
    print(f"\ntier0 deterministic handlers ({len(tiers['tier0'])}):")
    for label in tiers["tier0"]:
        print(f"  - {label}")

    print("\nrouting samples:")
    router = Router(paths, available_tiers=set(_tier_names(paths)))
    samples = [
        ("git status", "auto", True),
        ("what is the current branch?", "auto", True),
        ("queue depth?", "auto", True),
        ("summarize this diff in one line", "auto", True),
        ("write a UE5 UCLASS for a traversal component", "auto", True),
        ("review every file in the entire codebase", "auto", False),
        ("review every file in the entire codebase", "auto", True),
        ("do a thing", BATCH_TIER, True),
    ]
    for prompt, pref, interactive in samples:
        t = Task(task_id="SAMPLE", prompt=prompt, preferred_tier=pref, interactive=interactive)
        d = router.decide(t)
        flag = "" if interactive else " [background]"
        print(f"  {prompt[:48]:<50}{flag:<13} -> {d.tier}")
        print(f"      {d.reason}")
    return 0


def _tier_names(paths: Paths) -> list[str]:
    try:
        return list(BrainConfig.load(paths.brain_config).tiers)
    except BrainError:
        return []


def cmd_doctor(_: argparse.Namespace) -> int:
    import os

    paths = Paths.resolve()
    problems: list[str] = []

    print(f"python    : {sys.version.split()[0]} ({sys.executable})")
    print(f"workspace : {paths.root}  {'OK' if paths.root.exists() else 'MISSING'}")
    if not paths.root.exists():
        problems.append(f"workspace {paths.root} does not exist")

    for label, d in (
        ("queue/tasks", paths.tasks_dir),
        ("queue/processed", paths.processed_dir),
        ("state", paths.state_dir),
        ("config", paths.config_dir),
    ):
        print(f"  {label:<16} {'OK' if d.exists() else 'missing (run any command to create)'}")

    print("\ncredentials (names only, values never printed):")
    for var in ("GROQ_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY"):
        print(f"  {var:<20} {'set' if os.environ.get(var) else 'NOT SET'}")

    try:
        cfg = BrainConfig.load(paths.brain_config)
        print("\ntier readiness (config only, no network):")
        for name in cfg.tiers:
            try:
                cfg.build(name)
                print(f"  {name:<18} buildable")
            except BrainError as e:
                print(f"  {name:<18} {e}")
    except BrainError as e:
        problems.append(str(e))
        print(f"\nconfig: {e}")

    # Google Drive sync warning - MASTER_BLUEPRINT.md section 4.
    drive_hint = any(
        part.lower() in {"google drive", "googledrive", "my drive"}
        for part in paths.root.parts
    )
    if drive_hint:
        problems.append(
            "workspace looks like it sits inside a Google Drive folder; exclude "
            "AI_OS/queue and AI_OS/state from sync (blueprint section 4)"
        )

    print()
    if problems:
        for p in problems:
            print(f"[WARN] {p}")
        return 1
    print("[OK] no problems found")
    return 0


def cmd_submit(args: argparse.Namespace) -> int:
    transport = LocalFileTransport()
    task = Task(
        task_id=args.task_id or f"T-{int(time.time())}",
        prompt=args.prompt,
        sim_role=args.role,
        assigned_sim_id=args.sim,
        preferred_tier=args.tier,
        interactive=not args.background,
    )
    path = transport.enqueue(task)
    print(f"queued {task.task_id} -> {path}")
    if args.run:
        return 0 if Orchestrator().drain()[1] == 0 else 1
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    """Clear a task's processed/failed records so the id can run again.

    Needed because an earlier bug filed failed tasks into processed/, which the
    idempotency guard then treats as completed work forever.
    """
    paths = Paths.resolve().ensure()
    removed: list[str] = []
    for d in (paths.processed_dir, paths.failed_dir, paths.batch_dir, paths.inflight_dir):
        for p in sorted(d.glob(f"{args.task_id}*")):
            try:
                p.unlink()
                removed.append(str(p.relative_to(paths.root)))
            except OSError as e:
                print(f"could not remove {p}: {e}")
    if not removed:
        print(f"no records found for {args.task_id}")
        return 1
    for r in removed:
        print(f"removed {r}")
    print(f"{args.task_id} can now be submitted again")
    return 0


def cmd_once(_: argparse.Namespace) -> int:
    orch = Orchestrator()
    ok, fail = orch.drain()
    if ok == fail == 0:
        print("queue empty")
        return 0
    print(f"{ok} ok, {fail} failed")
    return 0 if fail == 0 else 1



_last_beat = 0.0


def _heartbeat(orch: "Orchestrator") -> None:
    """Touch state/brain.alive every few seconds so the Sims mod knows the brain is running."""
    global _last_beat
    now = time.time()
    if now - _last_beat < 5:
        return
    _last_beat = now
    f = orch.paths.hud_state.parent / "brain.alive"
    f.write_text(str(int(now)), encoding="utf-8")


def ingest_ratings(orch: "Orchestrator") -> int:
    """Pick up star ratings the Sims pie menu dropped in queue/ratings/ and attach them to task rows."""
    d = orch.paths.tasks_dir.parent / "ratings"
    if not d.exists():
        return 0
    rdir = orch.roster_dir
    n = 0
    for p in sorted(d.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            tid = str(data["task_id"])
            scores = {k: int(v) for k, v in (data.get("scores") or {}).items() if 0 <= int(v) <= 5}
        except (OSError, ValueError, KeyError, TypeError):
            p.rename(p.with_suffix(".bad"))
            continue
        hit = False
        for cat, val in scores.items():
            hit |= tracking.record_external(rdir, tid, f"user_{cat}", val, "user")
        if scores:
            hit |= tracking.record_external(rdir, tid, "user_stars", round(sum(scores.values()) / len(scores), 2), "user")
        done = d / "done"
        done.mkdir(exist_ok=True)
        p.replace(done / p.name)
        _log(f"rating for {tid}: {scores} ({'saved' if hit else 'no tracked task'})")
        n += 1
    return n


def cmd_serve(args: argparse.Namespace) -> int:
    orch = Orchestrator()
    _log(f"serving {orch.paths.tasks_dir}")
    ok, fail = orch.drain()  # catch up on anything queued while we were down
    if ok or fail:
        _log(f"startup drain: {ok} ok, {fail} failed")

    observer = _try_watchdog(orch)
    if observer is None:
        _log(f"watchdog unavailable; polling every {args.interval:g}s")

    _install_signal_handlers()
    try:
        while not _stop:
            try:
                _heartbeat(orch)
                ingest_ratings(orch)
            except Exception as e:  # ratings must never stop the brain
                _log(f"ratings ingest error: {e}")
            if observer is None:
                orch.drain()
                time.sleep(args.interval)
            else:
                time.sleep(0.5)
    finally:
        if observer is not None:
            observer.stop()
            observer.join(timeout=5)
        orch.transport.write_state(
            status="IDLE", task_description="Orchestrator stopped.", anim="idle"
        )
        _log("stopped")
    return 0


def _try_watchdog(orch: Orchestrator) -> Any:
    """Use watchdog if installed; otherwise fall back to polling.

    Deliberately optional: the orchestrator must run on a clean host with no
    pip install step.
    """
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        return None

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory and str(event.src_path).endswith(".json"):
                time.sleep(0.15)  # let the writer finish
                orch.drain()

        on_moved = on_created

    observer = Observer()
    observer.schedule(Handler(), str(orch.paths.tasks_dir), recursive=False)
    observer.daemon = True
    observer.start()
    _log("watching queue with watchdog")
    return observer


def _install_signal_handlers() -> None:
    def handler(_sig, _frame):
        global _stop
        _stop = True
        _log("shutdown requested")

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, handler)
        except (ValueError, OSError):
            pass


# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ai_os", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="show routing table and config").set_defaults(func=cmd_check)
    p_roster = sub.add_parser("roster", help="show Sim stats, or: roster suggest <prompt>")
    p_roster.add_argument("what", nargs="?", default="")
    p_roster.add_argument("rest", nargs="*")
    p_roster.set_defaults(func=cmd_roster)
    p_stats = sub.add_parser("stats", help="task-time/token/cost metrics per Sim")
    p_stats.add_argument("sim", nargs="?", default="")
    p_stats.set_defaults(func=cmd_stats)
    sub.add_parser("usage", help="today's usage against the free-tier caps").set_defaults(func=cmd_usage)
    p_rate = sub.add_parser("rate", help="rate a finished task 1-5 stars")
    p_rate.add_argument("task_id")
    p_rate.add_argument("stars", type=int)
    p_rate.set_defaults(func=cmd_rate)
    sub.add_parser("doctor", help="environment diagnostics").set_defaults(func=cmd_doctor)
    sub.add_parser("once", help="drain the queue once").set_defaults(func=cmd_once)

    p_serve = sub.add_parser("serve", help="run as a service")
    p_serve.add_argument("--interval", type=float, default=POLL_SECONDS)
    p_serve.set_defaults(func=cmd_serve)

    p_sub = sub.add_parser("submit", help="enqueue a task")
    p_sub.add_argument("prompt")
    p_sub.add_argument("--task-id")
    p_sub.add_argument("--role", default="coder")
    p_sub.add_argument("--sim", default="0413", help='Sim id, or "auto" to delegate by strength')
    p_sub.add_argument("--tier", default="auto")
    p_sub.add_argument("--background", action="store_true", help="nothing is waiting on this")
    p_sub.add_argument("--run", action="store_true", help="drain immediately after queueing")
    p_sub.set_defaults(func=cmd_submit)

    p_reset = sub.add_parser("reset", help="clear a task's records so its id can run again")
    p_reset.add_argument("task_id")
    p_reset.set_defaults(func=cmd_reset)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
