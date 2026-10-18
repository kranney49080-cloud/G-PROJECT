"""LAUNCHER 2 - agent key. Starts the Windows actrun agent so your PC can run pipeline jobs.
actrun.exe is looked for in: AI_OS\\vendor\\actionforge, then F:\\Downloads\\actrun-v0.16.11.cli-x64-windows.
The binary's own usage text is 'actrun agent --token <token>' (no --server flag is shown)."""
import os, subprocess, sys
from af_common import ask_key
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDIDATES = [
    os.path.join(BASE, "vendor", "actionforge", "actrun.exe"),
    r"F:\Downloads\actrun-v0.16.11.cli-x64-windows\actrun.exe",
]
EXE = next((p for p in CANDIDATES if os.path.exists(p)), None)
if not EXE:
    raise SystemExit("actrun.exe not found. Looked in:\n  " + "\n  ".join(CANDIDATES))
key = ask_key("AGENT token")
print("Using", EXE)
print("Starting agent. Close this window to stop it.")
sys.exit(subprocess.call([EXE, "agent", "--token", key]))
