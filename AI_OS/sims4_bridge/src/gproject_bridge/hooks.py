"""Starts the poller once the game is actually running a zone.

Wraps Zone.on_loading_screen_animation_finished (verified present in the game's
zone.pyc). The original runs first; our code only runs afterwards and can never
raise into the game.
"""
import functools

from gproject_bridge import poller
from gproject_bridge.log import log


def install():
    import zone
    target = zone.Zone
    original = target.on_loading_screen_animation_finished
    if getattr(original, "_gp_wrapped", False):
        return

    @functools.wraps(original)
    def wrapper(self, *args, **kwargs):
        result = original(self, *args, **kwargs)
        try:
            from gproject_bridge import brainlaunch
            brainlaunch.ensure_running()
        except Exception as exc:
            log("hook: brain launch failed (%s: %s)" % (type(exc).__name__, exc))
        try:
            poller.start()
        except Exception as exc:
            log("hook: poller.start failed (%s: %s)" % (type(exc).__name__, exc))
        try:
            from gproject_bridge import presence
            presence.start()
        except Exception as exc:
            log("hook: presence.start failed (%s: %s)" % (type(exc).__name__, exc))
        try:
            from gproject_bridge import glow
            glow.start()
        except Exception as exc:
            log("hook: glow.start failed (%s: %s)" % (type(exc).__name__, exc))
        return result

    wrapper._gp_wrapped = True
    target.on_loading_screen_animation_finished = wrapper
    log("hook: installed on Zone.on_loading_screen_animation_finished")
