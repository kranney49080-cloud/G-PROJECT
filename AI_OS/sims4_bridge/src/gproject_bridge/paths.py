"""Locate the Mods folder and config from inside a .ts4script zip.

Inside the game, this module's __file__ looks like
  ...\\Mods\\GProject\\GProjectBridge.ts4script\\gproject_bridge\\paths.pyc
so we walk up until we find the path component ending in .ts4script and use
its parent directory as the mod's home. Config and logs live there.
"""
import os

CONFIG_NAME = "bridge_config.json"
LOG_NAME = "gproject_bridge.log"


def mod_home():
    here = os.path.abspath(__file__)
    cur = here
    for _ in range(8):
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        if cur.lower().endswith(".ts4script"):
            return parent
        cur = parent
    # Not running from a zip (e.g. local test): use the package's parent folder.
    return os.path.dirname(os.path.dirname(here))


def config_path():
    return os.path.join(mod_home(), CONFIG_NAME)


def log_path():
    return os.path.join(mod_home(), LOG_NAME)
