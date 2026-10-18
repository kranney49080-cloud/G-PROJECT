"""Lot survey: lists every object on the lot to a JSON file so desks, computers,
fridges (our 'servers') and RGB lights can be mapped to office zones.

Written defensively: every attribute is read through getattr, and any failure
on one object is recorded and skipped. Never raises into the game.
"""
import json
import os

from gproject_bridge import config
from gproject_bridge.log import log

_LIGHT_WORDS = ("light", "dimmer", "color", "colour", "rgb")


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
            if n.startswith("_"):
                continue
            low = n.lower()
            if any(w in low for w in _LIGHT_WORDS):
                names.append("lighting_component." + n)
    for n in dir(obj):
        if n.startswith("_"):
            continue
        low = n.lower()
        if any(w in low for w in _LIGHT_WORDS):
            names.append(n)
    return sorted(set(names))[:40]


def run():
    """Returns (path, count). Raises only if the file cannot be written."""
    import services
    rows, errors = [], 0
    for obj in services.object_manager().get_all():
        try:
            if _safe(lambda: obj.is_sim, False):
                continue
            d = _safe(lambda: obj.definition)
            row = {
                "id": _safe(lambda: obj.id),
                "def_id": _safe(lambda: d.id),
                "name": _safe(lambda: str(d.name)),
                "cls": type(obj).__name__,
                "pos": _pos(obj),
                "level": _safe(lambda: obj.level),
                "has_light": _safe(lambda: obj.lighting_component is not None, False),
                "light_api": _light_api(obj) if _safe(lambda: obj.lighting_component is not None, False) else [],
            }
            rows.append(row)
        except Exception:
            errors += 1
    cfg = config.load()
    path = os.path.join(cfg["state_dir"], "lot_objects.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"count": len(rows), "errors": errors, "objects": rows}, fh, indent=1)
    os.replace(tmp, path)
    log("survey: wrote %d objects (%d errors) to %s" % (len(rows), errors, path))
    return path, len(rows)
