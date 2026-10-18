"""Stage (d): native in-game popups for HUD status changes.

Uses the game's own notification dialog (ui.ui_dialog_notification) with raw
text, so no string-table tuning is needed. Every call is guarded: a popup
problem is logged and never raised into the game. Verified against the game's
scripts: UiDialogNotification.TunableFactory().default(owner, title=, text=),
.show_dialog(), LocalizationHelperTuning.get_raw_text, services.active_sim_info.
"""
from gproject_bridge.log import log

TITLE = "G-Project AI OS"
MAX_TASK_CHARS = 90
MAX_ERROR_CHARS = 140
_STATUS_LABEL = {
    "IDLE": "Idle",
    "WORKING": "Working...",
    "COMPLETED": "Task complete",
    "FAILED": "Task FAILED",
}
_last_key = None


def format_message(data):
    """Pure function: status dict -> (title, text). Easy to test outside the game."""
    status = data.get("status", "?")
    role = data.get("assigned_role", "?")
    task = str(data.get("task_description", "")).replace("\n", " ").strip()
    if len(task) > MAX_TASK_CHARS:
        task = task[:MAX_TASK_CHARS - 3] + "..."
    lines = ["%s (%s)" % (_STATUS_LABEL.get(status, status), role)]
    if task:
        lines.append(task)
    if status == "FAILED" and data.get("error"):
        err = str(data["error"]).replace("\n", " ").strip()
        if len(err) > MAX_ERROR_CHARS:
            err = err[:MAX_ERROR_CHARS - 3] + "..."
        lines.append(err)
    stats = data.get("lifetime_stats") or {}
    if "success_rate" in stats:
        lines.append("Success rate: %s%%" % stats["success_rate"])
    return TITLE, "\n".join(lines)


def show(title, text):
    """Show one notification to the active Sim's player. Returns True if shown."""
    try:
        import services
        from sims4.localization import LocalizationHelperTuning
        from ui.ui_dialog_notification import UiDialogNotification
        owner = services.active_sim_info()
        if owner is None:
            log("notify: no active sim yet, skipped")
            return False
        notification = UiDialogNotification.TunableFactory().default(
            owner,
            title=lambda **_: LocalizationHelperTuning.get_raw_text(title),
            text=lambda **_: LocalizationHelperTuning.get_raw_text(text))
        notification.show_dialog()
        return True
    except Exception as exc:
        log("notify: failed (%s: %s)" % (type(exc).__name__, exc))
        return False


def on_status(data):
    """Called by the poller when a new valid status file was read."""
    global _last_key
    key = (data.get("status"), data.get("task_description"), data.get("updated_at"))
    if key == _last_key:
        return False
    _last_key = key
    title, text = format_message(data)
    ok = show(title, text)
    log("notify: %s status=%s" % ("shown" if ok else "not shown", data.get("status")))
    return ok
