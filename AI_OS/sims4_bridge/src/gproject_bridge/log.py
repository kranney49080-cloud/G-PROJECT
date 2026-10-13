"""Tiny file logger. Never raises: a logging failure must not break the game."""
import time

from gproject_bridge import paths

_MAX_BYTES = 512 * 1024


def log(msg):
    try:
        path = paths.log_path()
        try:
            import os
            if os.path.getsize(path) > _MAX_BYTES:
                os.replace(path, path + ".old")
        except OSError:
            pass
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("%s  %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg))
    except Exception:
        pass
