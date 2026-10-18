"""gp.dump: write every object on the lot (id, position, light API) to
state/lot_objects.json. Defensive: every attribute read is guarded; any failure on
one object is counted and skipped; nothing raises into the game.
"""
import os as _os, time as _time
def _early(msg):
    # Import-time breadcrumb in the mod's own folder (proves the module was imported).
    try:
        cur = _os.path.abspath(__file__)
        while cur and not cur.lower().endswith(".ts4script"):
            nxt = _os.path.dirname(cur)
            if nxt == cur:
                break
            cur = nxt
        home = _os.path.dirname(cur)
        with open(_os.path.join(home, "gproject_survey.log"), "a") as fh:
            fh.write("%s %s\n" % (_time.strftime("%H:%M:%S"), msg))
    except Exception:
        pass
_early("survey import begin")
import json
import os
import time

import sims4.commands

STATE_DIR = r"F:\MrMak\Workspace\AI_OS\state"
LOG = os.path.join(STATE_DIR, "survey.log")
_LIGHT_WORDS = ("light", "dimmer", "color", "colour", "rgb")


def _log(msg):
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write("%s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg))
    except Exception:
        pass


def _safe(fn, default=None):
    try:
        return fn()
    except Exception:
        return default


def _pos(obj):
    p = _safe(lambda: obj.position)
    if p is None:
        return None
    return [round(float(getattr(p, "x", 0)), 2), round(float(getattr(p, "y", 0)), 2),
            round(float(getattr(p, "z", 0)), 2)]


def _light_api(obj):
    names = []
    comp = _safe(lambda: obj.lighting_component)
    if comp is not None:
        for n in dir(comp):
            if not n.startswith("_") and any(w in n.lower() for w in _LIGHT_WORDS):
                names.append("lighting_component." + n)
    for n in dir(obj):
        if not n.startswith("_") and any(w in n.lower() for w in _LIGHT_WORDS):
            names.append(n)
    return sorted(set(names))[:40]


def _sims():
    """List every Sim currently in the game (id, name, household, position)."""
    import services
    out = []
    try:
        for si in services.sim_info_manager().get_all():
            sim = _safe(lambda: si.get_sim_instance())
            out.append({
                "sim_id": _safe(lambda: si.id),
                "name": _safe(lambda: "%s %s" % (si.first_name, si.last_name)),
                "household": _safe(lambda: si.household.name),
                "on_lot": sim is not None,
                "pos": _pos(sim) if sim is not None else None,
            })
    except Exception as exc:
        _log("sims list failed: %s: %s" % (type(exc).__name__, exc))
    return out


def _run():
    import services
    rows, errors = [], 0
    for obj in services.object_manager().get_all():
        try:
            if _safe(lambda: obj.is_sim, False):
                continue
            d = _safe(lambda: obj.definition)
            has_light = bool(_safe(lambda: obj.lighting_component is not None, False))
            rows.append({
                "id": _safe(lambda: obj.id),
                "def_id": _safe(lambda: d.id),
                "name": _safe(lambda: str(d.name)),
                "cls": type(obj).__name__,
                "pos": _pos(obj),
                "level": _safe(lambda: obj.level),
                "has_light": has_light,
                "light_api": _light_api(obj) if has_light else [],
            })
        except Exception:
            errors += 1
    path = os.path.join(STATE_DIR, "lot_objects.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"count": len(rows), "errors": errors, "sims": _sims(), "objects": rows}, fh, indent=1)
    os.replace(tmp, path)
    _log("wrote %d objects (%d errors) to %s" % (len(rows), errors, path))
    return path, len(rows)


@sims4.commands.Command("gp.dump", command_type=sims4.commands.CommandType.Live)
def gp_dump(_connection=None):
    _early("gp.dump called")
    try:
        path, n = _run()
        sims4.commands.output("G-Project: wrote %d objects to %s" % (n, path), _connection)
    except Exception as exc:
        _log("gp.dump failed: %s: %s" % (type(exc).__name__, exc))
        try:
            sims4.commands.output("G-Project: dump failed (%s: %s)" % (type(exc).__name__, exc), _connection)
        except Exception:
            pass


_log("survey module loaded")
_early("survey import done, gp.dump registered")


_SIM_OFF = (
    "stats.disable_all_commodities",      # needs stop decaying (verified in developer_commands)
    "autonomy.household off",            # Sims stop doing things on their own
    "death.toggle false",                # nobody dies
    "sims.set_aging_enabled_option false",  # no aging for the played household
    "sims.set_aging_unplayed_sims false",
)


def _apply_simoff(conn):
    done, failed = [], []
    for line in _SIM_OFF:
        try:
            sims4.commands.execute(line, conn)
            done.append(line)
        except Exception as exc:
            failed.append("%s (%s)" % (line, exc))
    _log("simoff ok=%d failed=%s" % (len(done), failed))
    return done, failed


@sims4.commands.Command("gp.simoff", command_type=sims4.commands.CommandType.Live)
def gp_simoff(_connection=None):
    """Turn the life simulation off: needs, autonomy, death, aging."""
    _early("gp.simoff called")
    done, failed = _apply_simoff(_connection)
    try:
        sims4.commands.output("G-Project: simulation off. ran %d, failed %d" % (len(done), len(failed)), _connection)
    except Exception:
        pass


def _install_auto_simoff():
    """Run simoff automatically every time a lot finishes loading (no typing needed)."""
    try:
        import functools
        import services
        from zone import Zone
        original = Zone.on_loading_screen_animation_finished
        if getattr(original, "_gp_simoff", False):
            return

        @functools.wraps(original)
        def wrapper(self, *args, **kwargs):
            result = original(self, *args, **kwargs)
            try:
                client = services.client_manager().get_first_client()
                _apply_simoff(client.id if client is not None else None)
                _early("auto simoff ran")
            except Exception as exc:
                _log("auto simoff failed: %s: %s" % (type(exc).__name__, exc))
            return result

        wrapper._gp_simoff = True
        Zone.on_loading_screen_animation_finished = wrapper
        _early("auto simoff hook installed")
    except Exception as exc:
        _log("auto simoff hook install failed: %s: %s" % (type(exc).__name__, exc))


_install_auto_simoff()
