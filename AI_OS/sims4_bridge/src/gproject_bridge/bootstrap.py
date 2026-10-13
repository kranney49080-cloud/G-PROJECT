"""Stage (a) entry point: proves the mod loaded. Runs at import, never raises."""
import sys

from gproject_bridge import __version__, paths
from gproject_bridge import config
from gproject_bridge.log import log


def _boot():
    log("=== G-Project bridge %s loaded ===" % __version__)
    log("python %s" % sys.version.replace("\n", " "))
    log("mod home: %s" % paths.mod_home())
    cfg = config.load()
    log("state_dir=%s poll_seconds=%s" % (cfg.get("state_dir"), cfg.get("poll_seconds")))
    from gproject_bridge import hooks
    hooks.install()


try:
    _boot()
except Exception as _exc:  # the game must always finish loading
    try:
        log("bootstrap error: %r" % (_exc,))
    except Exception:
        pass
