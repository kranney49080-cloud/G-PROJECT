"""Makes the "Ask the AI..." / "Rate last AI task..." entries appear on every Sim's pie menu.

The game defines Sim.super_affordances as a sims4.utils.flexmethod whose wrapped
function has the signature (cls, inst, context). We replace it with a new
flexmethod that yields everything the original yields, then our two tunings.
Never raises into the game from our own code.
"""
from gproject_bridge.log import log

AFFORDANCE_NAMES = ("GProject_AskBrain", "GProject_RateTask")
_cache = {"affs": None, "warned": False, "calls": 0}


def _find_affordances():
    if _cache["affs"] is not None:
        return _cache["affs"]
    import services
    import sims4.resources
    manager = services.get_instance_manager(sims4.resources.Types.INTERACTION)
    found = [t for t in manager.types.values() if getattr(t, "__name__", "") in AFFORDANCE_NAMES]
    if len(found) == len(AFFORDANCE_NAMES):
        _cache["affs"] = found
        log("inject: found %s" % ", ".join(t.__name__ for t in found))
        return found
    if not _cache["warned"]:
        _cache["warned"] = True
        log("inject: only %d of %d tunings loaded (is GProjectAskBrain.package installed?)" % (len(found), len(AFFORDANCE_NAMES)))
    return found


def install():
    from sims.sim import Sim
    from sims4.utils import flexmethod
    descriptor = Sim.__dict__.get("super_affordances")
    if descriptor is None or not hasattr(descriptor, "__wrapped_method__"):
        log("inject: Sim.super_affordances is not a flexmethod (%r); not wrapped" % (type(descriptor),))
        return
    original = descriptor.__wrapped_method__
    if getattr(original, "_gp_wrapped", False):
        return

    def wrapper(cls, inst, context=None):
        for aff in original(cls, inst, context):
            yield aff
        if inst is None:
            return
        try:
            _cache["calls"] += 1
            if _cache["calls"] in (1, 50, 500):
                log("inject: super_affordances called %d times" % _cache["calls"])
            extra = _find_affordances()
        except Exception as exc:
            extra = []
            if not _cache["warned"]:
                _cache["warned"] = True
                log("inject: lookup failed (%s: %s)" % (type(exc).__name__, exc))
        for aff in extra or ():
            yield aff

    wrapper._gp_wrapped = True
    Sim.super_affordances = flexmethod(wrapper)
    log("inject: wrapped Sim.super_affordances (flexmethod)")
