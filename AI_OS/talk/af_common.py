"""Shared helpers for the three Actionforge key launchers. Keys are typed in the window,
kept in memory only, and never written to a file. The screen is cleared after paste."""
import os, json, urllib.request, urllib.error
HOST = "https://orch.actionforge.dev"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Agentic3D-af/0.1"

def ask_key(label):
    k = os.environ.get("AF_KEY_OVERRIDE") or input("Paste the %s (right-click), then press Enter: " % label).strip()
    os.system("cls" if os.name == "nt" else "clear")
    if not k:
        raise SystemExit("No key given.")
    print("%s received (memory only, not saved)." % label)
    return k

def api(path, key, method="GET", body=None):
    h = {"Authorization": "Bearer " + key, "User-Agent": UA, "Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode(); h["Content-Type"] = "application/json"
    req = urllib.request.Request(HOST + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace") or "null")
    except urllib.error.HTTPError as e:
        return e.code, e.read(300).decode("utf-8", "replace").replace(key, "[key]")
