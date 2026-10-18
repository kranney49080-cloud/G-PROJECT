"""Actionforge Orchestrator -> in-game visual bridge (stdlib only).

Subscribes to the Orchestrator's live event streams (documented SSE endpoints):
    /api/v2/ci/runs/stream     all run updates
    /api/v2/ci/agents/stream   agent status changes
    /api/v2/ci/queue/stream    queue updates
and writes AI_OS\\state\\factory_state.json, which the Sims-side mod reads (same pattern as talk_state.json).

TOKEN: never stored in a file. Set env var ACTIONFORGE_TOKEN (a read-scoped personal access token)
or paste it when asked (cleared from the screen right after). It is only held in memory.

  py -3 factory_bridge.py --discover   print the first 15 raw events of each stream (token never printed)
  py -3 factory_bridge.py              run the bridge

NOTE: the event payload shape is not documented on the API page, so field names below are
partly verified: agents events are lists of {id, name, labels, status, registered_at, owner_user_id};
runs and queue arrive as lists (empty when idle). Run field names are still unverified until a run happens.
"""
import getpass, json, os, sys, threading, time, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ...\AI_OS
OUT = os.path.join(BASE, "state", "factory_state.json")
RAW = os.path.join(BASE, "state", "factory_raw_sample.jsonl")
HOST = "https://orch.actionforge.dev"
STREAMS = {"runs": "/api/v2/ci/runs/stream",
           "agents": "/api/v2/ci/agents/stream",
           "queue": "/api/v2/ci/queue/stream"}
STALE_RUN_SECONDS = 6 * 60 * 60   # a run with no update for this long is shown as idle

STATE = {"updated": 0, "connected": {}, "runs": {}, "agents": {}, "queue": 0}
LOCK = threading.Lock()

def norm_status(s):
    s = str(s or "").lower()
    if s in ("running", "in_progress", "started", "active", "busy"):
        return "running"
    if s in ("queued", "pending", "waiting", "scheduled"):
        return "queued"
    if s in ("success", "succeeded", "passed", "completed", "done", "ok"):
        return "success"
    if s in ("failed", "failure", "error", "errored"):
        return "failed"
    if s in ("cancelled", "canceled", "aborted"):
        return "cancelled"
    if s in ("online", "idle", "ready"):
        return "idle"
    if s in ("offline", "disconnected"):
        return "offline"
    return s or "unknown"

def pick(d, *keys):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return None

def save():
    with LOCK:
        STATE["updated"] = time.time()
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        tmp = OUT + ".tmp"
        with open(tmp, "w") as f:
            json.dump(STATE, f, indent=2)
        os.replace(tmp, OUT)

RAW_RUNS_LOGGED = [0]

def log_raw_run(data):
    """Keep the first 30 raw run events so the real field names can be read (no token involved)."""
    if RAW_RUNS_LOGGED[0] >= 30:
        return
    RAW_RUNS_LOGGED[0] += 1
    try:
        with open(RAW, "a") as f:
            f.write(json.dumps({"kind": "runs_live", "data": data}) + "\n")
    except OSError:
        pass

def apply(kind, data):
    if kind == "runs" and data:
        log_raw_run(data)
    is_list = isinstance(data, list)
    items = data if is_list else [data]
    with LOCK:
        if is_list and kind == "queue":      # observed: the queue arrives as a list of waiting runs
            STATE["queue"] = len(data)
            items = []
        if is_list and kind == "agents":     # observed: a full snapshot of every agent
            STATE["agents"] = {}
        for it in items:
            if not isinstance(it, dict):
                continue
            if kind == "runs":
                rid = str(pick(it, "id", "run_id", "runId") or "")
                if not rid:
                    continue
                STATE["runs"][rid] = {
                    "pipeline": pick(it, "pipeline", "workflow", "workflow_path", "name"),
                    "repo": pick(it, "repo", "repo_name", "project", "project_name", "name"),
                    "status": norm_status(pick(it, "status", "state", "conclusion")),
                    "agent": pick(it, "agent", "agent_name", "agent_id", "runner", "runner_name"),
                    "t": time.time(),
                }
            elif kind == "agents":
                name = str(pick(it, "name", "id", "agent") or "")
                if not name:
                    continue
                STATE["agents"][name] = {
                    "status": norm_status(pick(it, "status", "state")),
                    "labels": pick(it, "labels"),
                    "t": time.time(),
                }
            elif kind == "queue":
                q = pick(it, "length", "count", "size")
                if isinstance(q, int):
                    STATE["queue"] = q
        cutoff = time.time() - STALE_RUN_SECONDS
        for rid in [r for r, v in STATE["runs"].items() if v["t"] < cutoff]:
            del STATE["runs"][rid]
    save()

def stream(kind, path, token, discover, stop):
    backoff = 2
    seen = 0
    while not stop.is_set():
        try:
            req = urllib.request.Request(HOST + path, headers={
                "Authorization": "Bearer " + token, "Accept": "text/event-stream",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Agentic3D-bridge/0.2"})
            with urllib.request.urlopen(req, timeout=90) as r:
                with LOCK:
                    STATE["connected"][kind] = True
                save()
                print(time.strftime("%H:%M:%S"), kind, "connected", flush=True)
                backoff = 2
                buf = []
                for raw in r:
                    if stop.is_set():
                        return
                    line = raw.decode("utf-8", "replace").rstrip("\r\n")
                    if line.startswith("data:"):
                        buf.append(line[5:].lstrip())
                    elif line == "" and buf:
                        text = "\n".join(buf); buf = []
                        try:
                            data = json.loads(text)
                        except ValueError:
                            continue
                        if discover:
                            seen += 1
                            print(kind, json.dumps(data)[:600], flush=True)
                            with open(RAW, "a") as f:
                                f.write(json.dumps({"kind": kind, "data": data}) + "\n")
                            if seen >= 15:
                                return
                        else:
                            apply(kind, data)
        except Exception as e:  # network drop, timeout, 401, etc. (token is never in the message)
            msg = getattr(e, "code", None) or type(e).__name__
            print(time.strftime("%H:%M:%S"), kind, "stream problem:", msg, flush=True)
            try:  # show what the server said (a refusal reason, never our token)
                body = e.read(400).decode("utf-8", "replace").replace(token, "[token]")
                print("   server said:", body, flush=True)
                for h in ("Server", "CF-RAY", "WWW-Authenticate", "Content-Type"):
                    if e.headers.get(h):
                        print("   header", h + ":", e.headers.get(h), flush=True)
            except Exception:
                pass
        with LOCK:
            STATE["connected"][kind] = False
        if discover:
            return
        save()
        stop.wait(backoff)
        backoff = min(backoff * 2, 60)

def main():
    token = os.environ.get("ACTIONFORGE_TOKEN")
    if not token:
        # A normal prompt, because Windows' hidden prompt ignores right-click paste.
        # Right-click to paste, press Enter; the screen is cleared right after so the token is not left showing.
        token = input("Paste the Actionforge read-only token (right-click), then press Enter: ").strip()
        os.system("cls" if os.name == "nt" else "clear")
        print("Token received (kept in memory only, not saved).")
    if not token:
        print("No token given."); return
    discover = "--discover" in sys.argv
    stop = threading.Event()
    ts = [threading.Thread(target=stream, args=(k, p, token, discover, stop), daemon=True) for k, p in STREAMS.items()]
    for t in ts:
        t.start()
    try:
        while any(t.is_alive() for t in ts):
            time.sleep(1)
    except KeyboardInterrupt:
        stop.set()
    if discover:
        print("Done. Samples saved to", RAW)

if __name__ == "__main__":
    main()
