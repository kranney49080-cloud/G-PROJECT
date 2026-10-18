"""Pie-menu entry "Ask the AI..." shown on every Sim.

Pattern copied from the game's own sims.change_sim_name_interaction
(ImmediateSuperInteraction + a tunable UiDialogTextInputOkCancel, answers read
from dialog.text_input_responses). The tuning XML in the package points its
class attribute at AskBrainInteraction below.
"""
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from ui.ui_dialog_generic import UiDialogTextInputOkCancel

from gproject_bridge import notifier, taskqueue
from gproject_bridge.log import log

PROMPT_KEY = "prompt"


class AskBrainInteraction(ImmediateSuperInteraction):
    INSTANCE_TUNABLES = {
        "dialog": UiDialogTextInputOkCancel.TunableFactory(
            description="Text box where you type what the AI should do.",
            text_inputs=(PROMPT_KEY,),
        ),
    }

    def _run_interaction_gen(self, timeline):
        target = self.target if getattr(self.target, "is_sim", False) else self.sim
        sim_name = ""
        try:
            sim_name = target.sim_info.first_name or ""
        except Exception:
            pass

        def on_response(dialog):
            try:
                if not dialog.accepted:
                    return
                text = dialog.text_input_responses.get(PROMPT_KEY)
                if not text:
                    return
                task_id = taskqueue.submit(str(text), sim_name=sim_name)
                notifier.show("G-Project AI OS", "Task queued\n%s" % task_id)
            except Exception as exc:
                log("ask: submit failed (%s: %s)" % (type(exc).__name__, exc))
                notifier.show("G-Project AI OS", "Could not queue task:\n%s" % exc)

        try:
            dialog = self.dialog(self.sim, self.get_resolver())
            dialog.show_dialog(on_response=on_response)
        except Exception as exc:
            log("ask: dialog failed (%s: %s)" % (type(exc).__name__, exc))
        return True
        yield  # makes this a generator, as the game's own interactions are


RATE_KEYS = ("quality", "accuracy", "speed", "spec", "creativity")


class RateTaskInteraction(ImmediateSuperInteraction):
    """Rate the most recent finished task 0-5 in several categories."""
    INSTANCE_TUNABLES = {
        "dialog": UiDialogTextInputOkCancel.TunableFactory(
            description="Score boxes, each 0 to 5.",
            text_inputs=RATE_KEYS,
        ),
    }

    def _run_interaction_gen(self, timeline):
        def on_response(dialog):
            try:
                if not dialog.accepted:
                    return
                scores = {}
                for key in RATE_KEYS:
                    raw = str(dialog.text_input_responses.get(key) or "").strip()
                    if raw.isdigit() and 0 <= int(raw) <= 5:
                        scores[key] = int(raw)
                if not scores:
                    notifier.show("G-Project AI OS", "No scores entered (use 0 to 5).")
                    return
                task_id = taskqueue.submit_rating(scores)
                notifier.show("G-Project AI OS", "Rated %s\n%s" % (task_id, ", ".join("%s %d" % kv for kv in scores.items())))
            except Exception as exc:
                log("rate: failed (%s: %s)" % (type(exc).__name__, exc))
                notifier.show("G-Project AI OS", "Could not save rating:\n%s" % exc)

        try:
            dialog = self.dialog(self.sim, self.get_resolver())
            dialog.show_dialog(on_response=on_response)
        except Exception as exc:
            log("rate: dialog failed (%s: %s)" % (type(exc).__name__, exc))
        return True
        yield
