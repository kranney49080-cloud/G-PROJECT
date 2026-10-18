"""LAUNCHER 3 - broad/admin key. Checks the key works and shows what it can see. Nothing is changed.
Token strings returned by the server are always masked in the output."""
import re
from af_common import ask_key, api

def mask(o):
    if isinstance(o, dict):
        return {k: ("[hidden]" if k in ("token", "secret", "value", "password") else mask(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [mask(x) for x in o]
    if isinstance(o, str):
        return re.sub(r"bsp_[0-9a-fA-F]{8,}", "[hidden]", o)
    return o

key = ask_key("ADMIN (broad) Actionforge token")
for name, path in (("dashboard", "/api/v2/ci/dashboard"), ("agents", "/api/v2/ci/agents"),
                   ("queue", "/api/v2/ci/queue"), ("tokens", "/api/v2/ci/tokens")):
    code, data = api(path, key)
    print("\n== %s: HTTP %s" % (name, code))
    if code == 200:
        text = str(mask(data))
        print(text[:900] + (" ..." if len(text) > 900 else ""))
    else:
        print(mask(data))
print("\nDone. This tool only reads. To create pipelines use the Node Editor.")
