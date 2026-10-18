"""Agentic 3D presence: real-world AI activity -> Sim behaviour (the "Screen" side).

Reads two files written by the brain-side watchers (same state_dir as the HUD file):
  talk_state.json     {"chatgpt": {"active": bool, "since": ts}, "codex": {...}, "gemini": {...}}
  factory_state.json  {"runs": {id: {"status": "running"|...}}, "agents": {...}, "queue": n}

For every configured "actor" whose key is active, the Sim with that name is made to run one of the
game's OWN interactions (phone call / computer typing) through the game's normal interaction
queue (Sim.push_super_affordance, the same call the game's interactions.push cheat uses).
When the key goes inactive the interaction is cancelled.

Nothing here invents an animation: it only starts interactions the game already has. Which
interaction (tuning name) to use is config, because the names live in the game's tuning data.
On every zone load this module writes presence_interactions.txt (next to the mod) listing the
game's phone/computer/typing-like interaction names so they can be copied into the config.

Python 3.7 only (the game's version). Never raises into the game; every failure is logged.
"""
import json
import os
import time

from gproject_bridge import config, paths
from gproject_bridge.log import log

DEFAULT_PRESENCE = {
    "enabled": True,
    "poll_seconds": 2,
    "talk_file": "talk_state.json",
    "factory_file": "factory_state.json",
    # key in the state files -> which Sim, and which action ("phone" or "type")
    "actors": {
        "chatgpt": {"sim": "ChatGPT", "action": "phone"},
        "gemini": {"sim": "Gemini", "action": "phone"},
        "codex": {"sim": "Codex", "action": "type"},
    },
    # Optional: this Sim types while the Actionforge factory has any run "running". "" = off.
    "factory": {"sim": "", "action": "type"},
    # action -> list of interaction tuning names to try, in order. EMPTY until discovered:
    # copy names from presence_interactions.txt (written on every zone load).
    "interactions": {"phone": [], "type": []},
    # "self" = push on the Sim itself, "object" = find a nearby object offering the interaction.
    "targets": {"phone": "self", "type": "object"},
    "retry_seconds": 12,
    "max_failures": 5,
}

DISCOVER_WORDS = ("phone", "computer", "laptop", "typing", "tablet", "cell", "texting", "text_")


class _Owner(object):
    """Alarm owner; module global so the alarm's weak reference stays alive."""


_OWNER = _Owner()
_handle = None
_cfg = None
_ticks = 0
_applied = {}       # actor key -> True when we believe we started it
_failures = {}      # actor key -> consecutive failures
_next_try = {}      # actor key -> earliest real time for the next push
_overrides = {}     # actor key -> bool, set by `gp.presence test`
_warned = set()     # one-time warnings (missing Sim, unknown interaction name)
_name_map = None
status_lines = []   # last tick summary, shown by gp.presence


def _merge(base, extra):
    out = dict(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_cfg():
    return _merge(DEFAULT_PRESENCE, config.load().get("presence"))


def _state_path(cfg, key):
    return os.path.join(config.load()["state_dir"], cfg[key])


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            return json.load(fh)
    except Exception:
        return {}


def _warn_once(key, text):
    if key not in _warned:
        _warned.add(key)
        log("presence: " + text)


# ----------------------------------------------------------------- game lookups

def interaction_names():
    """{tuning name: class} for every loaded interaction tuning."""
    global _name_map
    if _name_map is not None:
        return _name_map
    import services
    import sims4.resources
    mgr = services.get_instance_manager(sims4.resources.Types.INTERACTION)
    out = {}
    for _key, cls in mgr.types.items():
        name = getattr(cls, "__name__", None)
        if name:
            out[name] = cls
    _name_map = out
    return out


def discover():
    """Write presence_interactions.txt with the interaction names that look relevant."""
    names = sorted(interaction_names())
    hits = [n for n in names if any(w in n.lower() for w in DISCOVER_WORDS)]
    path = os.path.join(paths.mod_home(), "presence_interactions.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# %s  %d interaction tunings loaded, %d match phone/computer/typing words\n"
                 % (time.strftime("%Y-%m-%d %H:%M:%S"), len(names), len(hits)))
        fh.write("# Copy names into bridge_config.json under presence.interactions.phone / .type\n")
        for n in hits:
            fh.write(n + "\n")
    log("presence: discovery wrote %d names (of %d) to %s" % (len(hits), len(names), path))
    return path, len(hits), len(names)


def find_sim(wanted):
    import services
    want = wanted.strip().lower()
    if not want:
        return None
    for sim in services.sim_info_manager().instanced_sims_gen():
        info = sim.sim_info
        full = ("%s %s" % (info.first_name, info.last_name)).strip().lower()
        if full == want or str(info.first_name).strip().lower() == want:
            return sim
    return None


def _find_object_target(sim, aff):
    """First valid object that offers `aff` to this Sim (e.g. a computer). Prefers the nearest."""
    import services
    best, best_d = None, None
    try:
        sim_pos = sim.position
    except Exception:
        sim_pos = None
    for obj in services.object_manager().valid_objects():
        try:
            if aff not in obj.super_affordances():
                continue
        except Exception:
            continue
        if sim_pos is None:
            return obj
        try:
            d = (obj.position - sim_pos).magnitude_squared()
        except Exception:
            d = 0
        if best is None or d < best_d:
            best, best_d = obj, d
    return best


def _running(sim, aff):
    try:
        return sim.find_interaction_by_affordance(aff) is not None
    except Exception:
        return False


def _push(sim, aff, target_mode):
    from interactions.context import InteractionContext
    from interactions.priority import Priority
    ctx = InteractionContext(sim, InteractionContext.SOURCE_SCRIPT, Priority.High)
    if target_mode == "object":
        target = _find_object_target(sim, aff)
        if target is None:
            return False, "no object offers it"
    else:
        target = sim
    result = sim.push_super_affordance(aff, target, ctx)
    return bool(result), str(result)


def _cancel(sim, aff):
    from interactions.interaction_finisher import FinishingType
    si = sim.find_interaction_by_affordance(aff)
    if si is not None:
        si.cancel(FinishingType.USER_CANCEL, cancel_reason_msg="Agentic 3D presence off")
        return True
    return False


# ----------------------------------------------------------------- the tick

def _desired(cfg):
    """{actor key: bool} from the two state files plus any test overrides."""
    out = {}
    talk = _read_json(_state_path(cfg, "talk_file"))
    for key in cfg["actors"]:
        entry = talk.get(key)
        out[key] = bool(isinstance(entry, dict) and entry.get("active"))
    fac = cfg.get("factory") or {}
    if fac.get("sim"):
        runs = (_read_json(_state_path(cfg, "factory_file")).get("runs") or {})
        out["_factory"] = any(isinstance(r, dict) and r.get("status") == "running"
                              for r in runs.values())
    for key, val in _overrides.items():
        out[key] = val
    return out


def _actor_cfg(cfg, key):
    if key == "_factory":
        return cfg["factory"]
    return cfg["actors"].get(key)


def _apply_one(cfg, key, want):
    actor = _actor_cfg(cfg, key)
    if not actor:
        return "?"
    names = cfg["interactions"].get(actor["action"]) or []
    if not names:
        _warn_once("noint-" + actor["action"],
                   "no interaction configured for action %r (see presence_interactions.txt)" % actor["action"])
        return "no-interaction-configured"
    sim = find_sim(actor["sim"])
    if sim is None:
        _warn_once("nosim-" + key, "Sim %r not in the game yet (actor %s)" % (actor["sim"], key))
        return "sim-missing"
    known = interaction_names()
    affs = []
    for n in names:
        if n in known:
            affs.append(known[n])
        else:
            _warn_once("unk-" + n, "unknown interaction name %r" % n)
    if not affs:
        return "no-valid-interaction"
    mode = cfg["targets"].get(actor["action"], "self")
    now = time.time()
    if want:
        if any(_running(sim, a) for a in affs):
            _applied[key] = True
            _failures[key] = 0
            return "running"
        if _failures.get(key, 0) >= cfg["max_failures"]:
            return "gave-up (toggle off/on to retry)"
        if now < _next_try.get(key, 0):
            return "waiting-retry"
        _next_try[key] = now + cfg["retry_seconds"]
        for a in affs:
            ok, why = _push(sim, a, mode)
            log("presence: push %s on %s -> %s (%s)" % (a.__name__, actor["sim"], ok, why))
            if ok:
                _applied[key] = True
                _failures[key] = 0
                return "pushed"
        _failures[key] = _failures.get(key, 0) + 1
        return "push-failed"
    # want is False
    _failures[key] = 0
    if _applied.get(key):
        for a in affs:
            if _cancel(sim, a):
                log("presence: cancelled %s on %s" % (a.__name__, actor["sim"]))
        _applied[key] = False
        return "cancelled"
    return "idle"


def _tick(_handle_arg=None):
    global _ticks
    _ticks += 1
    try:
        cfg = _cfg
        if cfg.get("enabled", True):
            want = _desired(cfg)
            lines = []
            for key, w in sorted(want.items()):
                try:
                    res = _apply_one(cfg, key, w)
                except Exception as exc:
                    res = "error %s: %s" % (type(exc).__name__, exc)
                    log("presence: %s error %s: %s" % (key, type(exc).__name__, exc))
                lines.append("%s want=%s -> %s" % (key, w, res))
            del status_lines[:]
            status_lines.extend(lines)
    except Exception as exc:
        log("presence: tick error %s: %s" % (type(exc).__name__, exc))
    try:
        _arm()
    except Exception as exc:
        log("presence: could not re-arm (%s: %s)" % (type(exc).__name__, exc))


def _arm():
    global _handle
    import alarms
    import clock
    _handle = alarms.add_alarm_real_time(
        _OWNER, clock.interval_in_real_seconds(_cfg["poll_seconds"]), _tick, repeating=False)


def start():
    """(Re)start. Safe on every zone load. Writes the discovery file once the game data is ready."""
    global _cfg, _ticks, _name_map
    _cfg = load_cfg()
    try:
        _cfg["poll_seconds"] = max(1, float(_cfg["poll_seconds"]))
    except Exception:
        _cfg["poll_seconds"] = 2.0
    stop()
    _ticks = 0
    _name_map = None
    _applied.clear()
    _failures.clear()
    try:
        discover()
    except Exception as exc:
        log("presence: discovery failed (%s: %s)" % (type(exc).__name__, exc))
    _arm()
    log("presence: started every %ss, enabled=%s, actors=%s" % (
        _cfg["poll_seconds"], _cfg.get("enabled", True), sorted(_cfg["actors"])))


def stop():
    global _handle
    if _handle is not None:
        try:
            import alarms
            alarms.cancel_alarm(_handle)
        except Exception:
            pass
        _handle = None


def set_override(key, value):
    """For `gp.presence test`: None clears the override."""
    if value is None:
        _overrides.pop(key, None)
    else:
        _overrides[key] = bool(value)
    _failures[key] = 0
    _next_try[key] = 0
