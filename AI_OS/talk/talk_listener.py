"""Phone -> PC "who am I talking to" listener (LAN only, stdlib only).
Phone shortcut calls:  http://<PC-IP>:8765/talk?who=gemini&on=1&token=<token>
                       http://<PC-IP>:8765/talk?who=gemini&on=0&token=<token>
Writes AI_OS\\state\\talk_state.json atomically. Token lives in AI_OS\\state\\talk_token.txt
(created on first run; keep it out of git)."""
import json, os, secrets, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ...\AI_OS
STATE = os.path.join(BASE, "state")
OUT = os.path.join(STATE, "talk_state.json")
TOK = os.path.join(STATE, "talk_token.txt")
PORT = 8765
WHO = {"gemini", "chatgpt"}
STALE_SECONDS = 3 * 60 * 60  # auto-clear if the phone never sends "off"

os.makedirs(STATE, exist_ok=True)
if not os.path.exists(TOK):
    with open(TOK, "w") as f:
        f.write(secrets.token_urlsafe(12))
TOKEN = open(TOK).read().strip()

def load():
    try:
        return json.load(open(OUT))
    except Exception:
        return {}

def save(d):
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, OUT)

def sweep(d):
    now = time.time()
    for k, v in d.items():
        if v.get("active") and now - v.get("since", now) > STALE_SECONDS:
            v["active"] = False
    return d

class H(BaseHTTPRequestHandler):
    def _reply(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if q.get("token") != TOKEN:
            return self._reply(403, {"ok": False, "error": "bad token"})
        if u.path == "/state":
            return self._reply(200, sweep(load()))
        if u.path != "/talk":
            return self._reply(404, {"ok": False})
        who = q.get("who", "").lower()
        if who not in WHO:
            return self._reply(400, {"ok": False, "error": "who must be gemini or chatgpt"})
        on = q.get("on", "1") in ("1", "true", "yes", "on")
        d = sweep(load())
        d[who] = {"active": on, "since": time.time()}
        save(d)
        print(time.strftime("%H:%M:%S"), who, "ON" if on else "off", flush=True)
        self._reply(200, {"ok": True, who: d[who]})

    do_POST = do_GET
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    save(sweep(load()))
    print("Talk listener on port %d" % PORT)
    print("Token file:", TOK)
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
