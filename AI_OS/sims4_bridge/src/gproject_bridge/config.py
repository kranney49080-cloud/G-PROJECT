"""Mod config. The polling target is defined here, not hardcoded (blueprint s4 rule 3)."""
import json

from gproject_bridge import paths
from gproject_bridge.log import log

DEFAULTS = {
    # Folder holding sim_hud_status.json (read) -- repoint here for a network share later.
    "state_dir": "F:\\MrMak\\Workspace\\AI_OS\\state",
    # Folder where the pie menu drops task files (written in stage c).
    "queue_tasks_dir": "F:\\MrMak\\Workspace\\AI_OS\\queue\\tasks",
    "status_file": "sim_hud_status.json",
    # Real-time poll interval in seconds (stage b). Real time, so pausing the game does not freeze it.
    "poll_seconds": 3,
    # Native popup on every HUD status change (stage d).
    "popups_enabled": True,
    # Task submission (stage c). Empty = use the Sim/role from the HUD file.
    "default_sim_id": "",
    "default_role": "",
    "preferred_tier": "auto",
}


def load():
    cfg = dict(DEFAULTS)
    try:
        with open(paths.config_path(), "r", encoding="utf-8-sig") as fh:
            cfg.update(json.load(fh))
    except Exception as exc:
        log("config: using defaults (%s: %s)" % (type(exc).__name__, exc))
    return cfg
