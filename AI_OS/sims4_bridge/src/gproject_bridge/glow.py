"""Status glow: show each AI Sim's status as the game's own pulsing colored outline.

The game already has a "call to action" highlight (the glowing outline used by tutorials).
Its code sends one network op to any object or Sim:
    Distributor.instance().add_op(sim, SetCallToAction(color, speed, thickness))
and turns it off with SetCallToAction(0, 0, 0). This module does exactly that, per Sim, from
the same state the rest of the mod reads. The color is ARGB (0xAARRGGBB), speed = pulses, and
thickness is a float (the game's own tuning allows 0.001-0.005; larger is untested).

Status sources, strongest first:
  1. gp.glow test overrides
  2. the HUD file (sim_hud_status.json: sim_id + status WORKING/COMPLETED/FAILED/IDLE); the
     sim_id is turned into a Sim name through config/staff.json
  3. presence: an actor that is active in talk_state.json (ChatGPT on the phone, Codex typing)
     or the factory Sim while an Actionforge run is running  -> "working"

  gp.glow                       show what each Sim is showing
  gp.glow test <name> <working|completed|failed|off|clear>
  gp.glow size <number>         change the outline thickness for all styles (try 0.004, 0.006, 0.01)
  gp.glow off                   switch every glow off

Python 3.7 only. Never raises into the game.
"""
import json
import os
import time

from gproject_bridge import config
from gproject_bridge.log import log

DEFAULT_GLOW = {
    "enabled": True,
    "poll_seconds": 2,
    "completed_seconds": 30,   # green stays this long, then the outline switches off
    "size": 0.0,               # 0 = use each style's own thickness
    # status -> [color ARGB, pulse speed, thickness]; None = no outline
    "styles": {
        "working": [0xFF2D8CFF, 1.0, 0.004],     # blue, steady pulse
        "completed": [0xFF2ECC40, 0.2, 0.004],   # green, slow
        "failed": [0xFFFF3B30, 3.0, 0.005],      # red, fast
        "idle": None,
    },
}


class _Owner(object):
    """Alarm owner; module global so the alarm's weak reference stays alive."""


_OWNER = _Owner()
_handle = None
_cfg = None
_applied = {}      # sim_id -> status currently shown
_since = {}        # name -> (status, first seen real time) for the completed timeout
_overrides = {}    # lower name -> status or "off"
_size_override = [None]
_names = None
status_lines = []


def _merge(base, extra):
    out = dict(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_cfg():
    return _merge(DEFAULT_GLOW, config.load().get("glow"))


def _staff_names():
    """{'0417': 'claude', ...} from config/staff.json."""
    global _names
    if _names is not None:
        return _names
    out = {}
    try:
        path = os.path.join(os.path.dirname(config.load()["state_dir"].rstrip("\\/")), "config", "staff.json")
        with open(path, "r", encoding="utf-8-sig") as fh:
            for e in json.load(fh).get("staff", []):
                out[str(e.get("sim_id"))] = str(e.get("name", "")).lower()
    except Exception as exc:
        log("glow: staff.json unreadable (%s: %s)" % (type(exc).__name__, exc))
    _names = out
    return out


def _wanted():
    """{sim name (lower): status} from every source."""
    want = {}
    # presence actors and the factory Sim -> working
    try:
        from gproject_bridge import presence
        if presence._cfg:
            for key, active in presence._desired(presence._cfg).items():
                if not active:
                    continue
                actor = presence._actor_cfg(presence._cfg, key)
                if actor and actor.get("sim"):
                    want[actor["sim"].strip().lower()] = "working"
    except Exception as exc:
        log("glow: presence read failed (%s: %s)" % (type(exc).__name__, exc))
    # HUD status from the brain
    try:
        from gproject_bridge import poller
        cur = poller.current
        if cur:
            name = _staff_names().get(str(cur.get("sim_id")))
            status = str(cur.get("status", "")).lower()
            if name and status in ("working", "completed", "failed", "idle"):
                want[name] = status
    except Exception as exc:
        log("glow: HUD read failed (%s: %s)" % (type(exc).__name__, exc))
    for name, status in _overrides.items():
        want[name] = status
    return want


def _style(cfg, status):
    st = cfg["styles"].get(status)
    if not st:
        return None
    color, speed, thick = st
    size = _size_override[0] if _size_override[0] is not None else cfg.get("size", 0.0)
    if size:
        thick = float(size)
    return int(color), float(speed), float(thick)


def _send(sim, style):
    from distributor.ops import SetCallToAction
    from distributor.system import Distributor
    if style is None:
        op = SetCallToAction(0, 0, 0)
    else:
        op = SetCallToAction(style[0], style[1], style[2])
    Distributor.instance().add_op(sim, op)


def _tick(_handle_arg=None):
    try:
        cfg = _cfg
        if cfg.get("enabled", True):
            import services
            want = _wanted()
            now = time.time()
            lines = []
            for sim in services.sim_info_manager().instanced_sims_gen():
                info = sim.sim_info
                names = (str(info.first_name).strip().lower(),
                         ("%s %s" % (info.first_name, info.last_name)).strip().lower())
                status = None
                for n in names:
                    if n in want:
                        status = want[n]
                        break
                if status == "off":
                    status = "idle"
                if status is None:
                    status = "idle"
                key = names[0]
                if status == "completed":
                    prev = _since.get(key)
                    if not prev or prev[0] != "completed":
                        _since[key] = ("completed", now)
                    elif now - prev[1] > cfg["completed_seconds"]:
                        status = "idle"
                else:
                    _since.pop(key, None)
                shown = (status, _style(cfg, status))
                prev = _applied.get(sim.sim_id)
                if prev != shown:
                    _send(sim, shown[1])
                    _applied[sim.sim_id] = shown
                    if status != "idle" or prev is not None:
                        log("glow: %s -> %s" % (info.first_name, status))
                if status != "idle":
                    lines.append("%s: %s" % (info.first_name, status))
            del status_lines[:]
            status_lines.extend(lines or ["(no Sim is glowing)"])
    except Exception as exc:
        log("glow: tick error %s: %s" % (type(exc).__name__, exc))
    try:
        _arm()
    except Exception as exc:
        log("glow: could not re-arm (%s: %s)" % (type(exc).__name__, exc))


def _arm():
    global _handle
    import alarms
    import clock
    _handle = alarms.add_alarm_real_time(
        _OWNER, clock.interval_in_real_seconds(_cfg["poll_seconds"]), _tick, repeating=False)


def start():
    global _cfg
    _cfg = load_cfg()
    try:
        _cfg["poll_seconds"] = max(1, float(_cfg["poll_seconds"]))
    except Exception:
        _cfg["poll_seconds"] = 2.0
    stop()
    _applied.clear()
    _arm()
    log("glow: started every %ss, enabled=%s" % (_cfg["poll_seconds"], _cfg.get("enabled", True)))


def stop():
    global _handle
    if _handle is not None:
        try:
            import alarms
            alarms.cancel_alarm(_handle)
        except Exception:
            pass
        _handle = None


def all_off():
    import services
    for sim in services.sim_info_manager().instanced_sims_gen():
        try:
            _send(sim, None)
        except Exception:
            pass
    _applied.clear()
    _overrides.clear()


def set_override(name, status):
    key = name.strip().lower()
    if status == "clear":
        _overrides.pop(key, None)
    else:
        _overrides[key] = status
    _applied.clear()


def set_size(value):
    _size_override[0] = float(value)
    _applied.clear()
