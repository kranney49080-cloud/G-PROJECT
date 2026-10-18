"""PC mic -> "who am I talking to" watcher (Windows only, stdlib only).
Windows records which app is using the microphone under
HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone
While an app holds the mic, its LastUsedTimeStop is 0. We watch for the ChatGPT app (not Codex)
and write AI_OS\\state\\talk_state.json, the same file the phone listener writes.

  py -3 mic_watcher.py --discover    list every app using the mic for 30 s (use this first)
  py -3 mic_watcher.py               run the watcher
"""
import json, os, sys, time, winreg

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ...\AI_OS
OUT = os.path.join(BASE, "state", "talk_state.json")
KEY = r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone"

# who -> (name must contain one of these, name must not contain any of these)
WHO = {"chatgpt": (["chatgpt"], ["codex"])}
ON_AFTER = 2      # consecutive polls with the mic held before we say "on"
OFF_AFTER = 5     # consecutive polls without it before we say "off"
POLL = 1.5

def scan():
    rows = []
    for sub in ("", "\\NonPackaged"):
        try:
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY + sub)
        except OSError:
            continue
        i = 0
        while True:
            try:
                name = winreg.EnumKey(k, i)
            except OSError:
                break
            i += 1
            if name == "NonPackaged":
                continue
            try:
                sk = winreg.OpenKey(k, name)
                start = winreg.QueryValueEx(sk, "LastUsedTimeStart")[0]
                stop = winreg.QueryValueEx(sk, "LastUsedTimeStop")[0]
            except OSError:
                continue
            rows.append((name.replace("#", "\\"), start, stop, start > 0 and stop <= start))
    return rows

def load():
    try:
        return json.load(open(OUT))
    except Exception:
        return {}

def save(d):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".mic.tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, OUT)

def holding(rows, want, avoid):
    for name, _s, _t, active in rows:
        n = name.lower()
        if active and any(w in n for w in want) and not any(a in n for a in avoid):
            return name
    return None

def discover():
    print("Start a ChatGPT voice chat now. Listing apps that hold the microphone (30 s)...")
    seen = {}
    t0 = time.time()
    while time.time() - t0 < 30:
        for name, _s, _t, active in scan():
            if active and name not in seen:
                seen[name] = time.strftime("%H:%M:%S")
                print(seen[name], "MIC IN USE:", name, flush=True)
        time.sleep(1)
    if not seen:
        print("No app was holding the microphone.")
    print("Done. Close this window.")

def watch():
    print("Mic watcher running. Close this window to stop.")
    streak = {w: 0 for w in WHO}
    miss = {w: 0 for w in WHO}
    on = {w: False for w in WHO}
    while True:
        rows = scan()
        for who, (want, avoid) in WHO.items():
            hit = holding(rows, want, avoid)
            if hit:
                streak[who] += 1; miss[who] = 0
            else:
                miss[who] += 1; streak[who] = 0
            d = None
            if not on[who] and streak[who] >= ON_AFTER:
                d = load(); d[who] = {"active": True, "since": time.time(), "source": "pc_mic"}
                on[who] = True
                print(time.strftime("%H:%M:%S"), who, "ON via", hit, flush=True)
            elif on[who] and miss[who] >= OFF_AFTER:
                d = load()
                if d.get(who, {}).get("source") == "pc_mic":
                    d[who] = {"active": False, "since": time.time(), "source": "pc_mic"}
                on[who] = False
                print(time.strftime("%H:%M:%S"), who, "off", flush=True)
            if d is not None:
                save(d)
        time.sleep(POLL)

if __name__ == "__main__":
    discover() if "--discover" in sys.argv else watch()
