"""Cheat-console commands (open the console with Ctrl+Shift+C):

  gp.task <your request>   queue a task for the brain
  gp.status                show the HUD's last status
  gp.dump                  write every lot object (id, position, light API) to state/lot_objects.json
  gp.presence              show what the Sims are doing for the AIs
  gp.presence test <who> on|off|clear   force an actor on/off to test (who = chatgpt, codex, gemini)
  gp.interactions          rewrite presence_interactions.txt (phone/computer interaction names)
  gp.roster [apply|undo]   rename household Sims to the AI names (no argument = dry run)
  gp.glow                  show status outlines; gp.glow test <name> <working|completed|failed|off|clear>
                           gp.glow size <number>  |  gp.glow off

Verified against the game's scripts: sims4.commands.Command(*aliases,
command_type=...), CommandType.Live, sims4.commands.output(text, context).
"""
import sims4.commands

from gproject_bridge import notifier, poller, survey, taskqueue
from gproject_bridge.log import log


def _say(text, connection):
    try:
        sims4.commands.output(text, connection)
    except Exception as exc:
        log("cmd: output failed (%s: %s)" % (type(exc).__name__, exc))


@sims4.commands.Command("gp.task", command_type=sims4.commands.CommandType.Live)
def gp_task(*words, _connection=None):
    prompt = " ".join(words).strip()
    if not prompt:
        _say("Usage: gp.task <what you want the AI to do>", _connection)
        return
    try:
        task_id = taskqueue.submit(prompt)
    except Exception as exc:
        log("cmd: gp.task failed (%s: %s)" % (type(exc).__name__, exc))
        _say("G-Project: could not queue task (%s)" % exc, _connection)
        notifier.show("G-Project AI OS", "Could not queue task:\n%s" % exc)
        return
    _say("G-Project: queued %s" % task_id, _connection)
    notifier.show("G-Project AI OS", "Task queued\n%s" % task_id)


@sims4.commands.Command("gp.status", command_type=sims4.commands.CommandType.Live)
def gp_status(_connection=None):
    cur = poller.current
    if not cur:
        _say("G-Project: no status read yet", _connection)
        return
    title, text = notifier.format_message(cur)
    _say(text, _connection)


@sims4.commands.Command("gp.dump", command_type=sims4.commands.CommandType.Live)
def gp_dump(_connection=None):
    try:
        path, n = survey.run()
    except Exception as exc:
        log("cmd: gp.dump failed (%s: %s)" % (type(exc).__name__, exc))
        _say("G-Project: dump failed (%s: %s)" % (type(exc).__name__, exc), _connection)
        return
    _say("G-Project: wrote %d objects to %s" % (n, path), _connection)


@sims4.commands.Command("gp.presence", command_type=sims4.commands.CommandType.Live)
def gp_presence(*words, _connection=None):
    from gproject_bridge import presence
    words = [w.lower() for w in words]
    try:
        if len(words) >= 3 and words[0] == "test":
            who, mode = words[1], words[2]
            if mode not in ("on", "off", "clear"):
                _say("Usage: gp.presence test <who> on|off|clear", _connection)
                return
            presence.set_override(who, None if mode == "clear" else mode == "on")
            _say("G-Project: presence test %s %s (takes effect within a few seconds)" % (who, mode), _connection)
            return
        lines = list(presence.status_lines) or ["(no tick yet - load a lot first)"]
        for line in lines:
            _say("presence: " + line, _connection)
    except Exception as exc:
        log("cmd: gp.presence failed (%s: %s)" % (type(exc).__name__, exc))
        _say("G-Project: presence failed (%s: %s)" % (type(exc).__name__, exc), _connection)


@sims4.commands.Command("gp.interactions", command_type=sims4.commands.CommandType.Live)
def gp_interactions(_connection=None):
    from gproject_bridge import presence
    try:
        presence._name_map = None
        path, hits, total = presence.discover()
    except Exception as exc:
        log("cmd: gp.interactions failed (%s: %s)" % (type(exc).__name__, exc))
        _say("G-Project: discovery failed (%s: %s)" % (type(exc).__name__, exc), _connection)
        return
    _say("G-Project: %d of %d interactions match, written to %s" % (hits, total, path), _connection)


@sims4.commands.Command("gp.roster", command_type=sims4.commands.CommandType.Live)
def gp_roster(*words, _connection=None):
    from gproject_bridge import roster
    mode = words[0].lower() if words else "show"
    try:
        if mode == "apply":
            lines = roster.apply()
        elif mode == "undo":
            lines = roster.undo()
        else:
            lines = ["(dry run - type gp.roster apply to rename)"] + roster.show()
        for line in lines:
            _say("roster: " + line, _connection)
    except Exception as exc:
        log("cmd: gp.roster failed (%s: %s)" % (type(exc).__name__, exc))
        _say("G-Project: roster failed (%s: %s)" % (type(exc).__name__, exc), _connection)


@sims4.commands.Command("gp.glow", command_type=sims4.commands.CommandType.Live)
def gp_glow(*words, _connection=None):
    from gproject_bridge import glow
    w = list(words)
    try:
        if len(w) >= 3 and w[0].lower() == "test":
            status = w[-1].lower()
            name = " ".join(w[1:-1])
            if status not in ("working", "completed", "failed", "off", "clear"):
                _say("Usage: gp.glow test <name> working|completed|failed|off|clear", _connection)
                return
            glow.set_override(name, status)
            _say("G-Project: glow test %s = %s (applies within a few seconds)" % (name, status), _connection)
        elif len(w) == 2 and w[0].lower() == "size":
            glow.set_size(w[1])
            _say("G-Project: outline thickness set to %s" % w[1], _connection)
        elif w and w[0].lower() == "off":
            glow.all_off()
            _say("G-Project: all glows off", _connection)
        else:
            for line in (list(glow.status_lines) or ["(no tick yet - load a lot first)"]):
                _say("glow: " + line, _connection)
    except Exception as exc:
        log("cmd: gp.glow failed (%s: %s)" % (type(exc).__name__, exc))
        _say("G-Project: glow failed (%s: %s)" % (type(exc).__name__, exc), _connection)
