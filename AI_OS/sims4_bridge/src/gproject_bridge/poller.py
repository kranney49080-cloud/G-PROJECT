"""Stage (b): real-time poller for sim_hud_status.json.

Uses the game's own alarm service in REAL time (alarms.add_alarm_real_time), so
pausing the game does not freeze the HUD. time.sleep() is never used.
The alarm is one-shot and re-armed after every tick: if a tick ever fails, the
next one still happens, and a zone change simply cancels it until restart().
Verified against the game's scripts: add_alarm_real_time(owner, time_span,
callback, repeating, use_sleep_time, cross_zone); callback receives the handle.
"""
import json
import os

from gproject_bridge import config
from gproject_bridge.log import log

REQUIRED_KEYS = ("sim_id", "status", "assigned_role", "task_description", "visual_cues")
VALID_STATUS = ("IDLE", "WORKING", "COMPLETED", "FAILED")
HEARTBEAT_TICKS = 100


class _Owner(object):
    """Alarm owner. Must stay alive (module global) - alarms hold only a weakref."""


_OWNER = _Owner()
_handle = None
_cfg = None
_last_mtime = None
_last_bad_mtime = None
_ticks = 0
current = None  # latest validated status dict (consumed by stages c/d)


def _status_path():
    return os.path.join(_cfg["state_dir"], _cfg["status_file"])


def _validate(data):
    if not isinstance(data, dict):
        return "top-level JSON is not an object"
    for key in REQUIRED_KEYS:
        if key not in data:
            return "missing key %r" % key
    if data["status"] not in VALID_STATUS:
        return "bad status %r" % (data["status"],)
    if not isinstance(data["visual_cues"], dict):
        return "visual_cues is not an object"
    return None


def read_once():
    """Read the status file if it changed. Returns True when `current` was updated."""
    global current, _last_mtime, _last_bad_mtime
    path = _status_path()
    try:
        mtime = os.stat(path).st_mtime
    except OSError:
        return False  # file absent: the brain has not written yet
    if mtime == _last_mtime or mtime == _last_bad_mtime:
        return False
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except Exception as exc:
        _last_bad_mtime = mtime
        log("poll: unreadable status file (%s: %s)" % (type(exc).__name__, exc))
        return False
    problem = _validate(data)
    if problem:
        _last_bad_mtime = mtime
        log("poll: invalid status file (%s)" % problem)
        return False
    _last_mtime = mtime
    current = data
    cues = data.get("visual_cues", {})
    log("poll: status=%s role=%s anim=%s task=%s" % (
        data["status"], data["assigned_role"], cues.get("anim"),
        str(data["task_description"])[:60]))
    return True


def _arm():
    global _handle
    import alarms
    import clock
    _handle = alarms.add_alarm_real_time(
        _OWNER, clock.interval_in_real_seconds(_cfg["poll_seconds"]), _tick,
        repeating=False)


def _tick(_handle_arg=None):
    global _ticks
    _ticks += 1
    try:
        read_once()
        if _ticks == 1 or _ticks % HEARTBEAT_TICKS == 0:
            log("poll: alive, ticks=%d" % _ticks)
    except Exception as exc:
        log("poll: tick error %s: %s" % (type(exc).__name__, exc))
    try:
        _arm()
    except Exception as exc:
        log("poll: could not re-arm alarm (%s: %s)" % (type(exc).__name__, exc))


def start():
    """(Re)start polling. Safe to call repeatedly (e.g. on every zone load)."""
    global _cfg, _ticks
    _cfg = config.load()
    try:
        _cfg["poll_seconds"] = max(1, float(_cfg["poll_seconds"]))
    except Exception:
        _cfg["poll_seconds"] = 3.0
    stop()
    _ticks = 0
    _arm()
    log("poll: started, every %ss, file=%s" % (_cfg["poll_seconds"], _status_path()))


def stop():
    global _handle
    if _handle is not None:
        try:
            import alarms
            alarms.cancel_alarm(_handle)
        except Exception:
            pass
        _handle = None
