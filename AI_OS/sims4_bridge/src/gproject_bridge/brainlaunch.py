"""Starts the Python brain when the game loads, if it is not already running.

The brain touches state/brain.alive every ~5s. If that file is missing or older
than STALE_SECONDS, we run the launcher (start_brain.bat) once per game session.
Never raises into the game.
"""
import os
import time

from gproject_bridge import config
from gproject_bridge.log import log

STALE_SECONDS = 30
_started = {"done": False}


def _alive(cfg):
    path = os.path.join(cfg["state_dir"], "brain.alive")
    try:
        return time.time() - os.path.getmtime(path) < STALE_SECONDS
    except OSError:
        return False


def ensure_running():
    if _started["done"]:
        return
    _started["done"] = True
    cfg = config.load()
    if not cfg.get("autostart_brain", True):
        return
    if _alive(cfg):
        log("brain: already running")
        return
    launcher = cfg.get("brain_launcher") or r"F:\MrMak\Workspace\AI_OS\start_brain.bat"
    if not os.path.exists(launcher):
        log("brain: launcher not found: %s" % launcher)
        return
    try:
        os.startfile(launcher)
        log("brain: launched %s" % launcher)
    except Exception as exc:
        log("brain: startfile failed (%s: %s)" % (type(exc).__name__, exc))
        try:
            import subprocess
            subprocess.Popen(["cmd", "/c", launcher], cwd=os.path.dirname(launcher))
            log("brain: launched via subprocess")
        except Exception as exc2:
            log("brain: launch failed (%s: %s)" % (type(exc2).__name__, exc2))
