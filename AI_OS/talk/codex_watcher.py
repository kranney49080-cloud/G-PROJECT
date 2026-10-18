"""Codex "is working" watcher (stdlib only). Reads file sizes/times ONLY, never file contents.
Codex keeps writing to its log database while it works, so we watch the write-ahead log
C:\\Users\\<you>\\.codex\\logs_2.sqlite-wal (and newest rollout file, if any).
Result goes into AI_OS\\state\\talk_state.json under the key "codex" (source "codex_log").

  py -3 codex_watcher.py --discover   60 s of change log: run once while Codex is idle, once while it works
  py -3 codex_watcher.py              run the watcher
"""
import json, os, sys, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ...\AI_OS
OUT = os.path.join(BASE, "state", "talk_state.json")
CODEX = os.path.join(os.path.expanduser("~"), ".codex")
WATCH = [os.path.join(CODEX, "logs_2.sqlite-wal")]
SESS = os.path.join(CODEX, "sessions")

ON_WINDOW = 6      # seconds: a change this recent means working
OFF_AFTER = 25     # seconds of no change before we say idle
POLL = 1.0

def newest_rollout():
    best, bt = None, 0
    try:
        for r, _d, fs in os.walk(SESS):
            for f in fs:
                if f.startswith("rollout-"):
                    p = os.path.join(r, f)
                    t = os.path.getmtime(p)
                    if t > bt:
                        best, bt = p, t
    except OSError:
        pass
    return best

def stamp(paths):
    out = {}
    for p in paths:
        try:
            s = os.stat(p); out[p] = (s.st_size, s.st_mtime)
        except OSError:
            out[p] = None
    return out

def load():
    try:
        return json.load(open(OUT))
    except Exception:
        return {}

def save(d):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".codex.tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, OUT)

def discover():
    print("Logging changes for 60 s. Run once with Codex idle, once while it is working on something.")
    prev, t0, n = None, time.time(), 0
    while time.time() - t0 < 60:
        paths = WATCH + ([newest_rollout()] if newest_rollout() else [])
        cur = stamp(paths)
        if prev is not None:
            for p, v in cur.items():
                if prev.get(p) != v:
                    n += 1
                    print(time.strftime("%H:%M:%S"), "CHANGED", os.path.basename(p), v, flush=True)
        prev = cur
        time.sleep(1)
    print("Total changes in 60 s:", n)
    print("Done. Close this window.")

def watch():
    print("Codex watcher running. Close this window to stop.")
    prev, last_change, on = None, 0.0, False
    while True:
        paths = WATCH + ([newest_rollout()] if newest_rollout() else [])
        cur = stamp(paths)
        if prev is not None and any(prev.get(p) != v for p, v in cur.items()):
            last_change = time.time()
        prev = cur
        quiet = time.time() - last_change
        if not on and quiet <= ON_WINDOW and last_change:
            d = load(); d["codex"] = {"active": True, "since": time.time(), "source": "codex_log"}
            save(d); on = True
            print(time.strftime("%H:%M:%S"), "codex ON", flush=True)
        elif on and quiet >= OFF_AFTER:
            d = load()
            if d.get("codex", {}).get("source") == "codex_log":
                d["codex"] = {"active": False, "since": time.time(), "source": "codex_log"}
                save(d)
            on = False
            print(time.strftime("%H:%M:%S"), "codex off", flush=True)
        time.sleep(POLL)

if __name__ == "__main__":
    discover() if "--discover" in sys.argv else watch()
