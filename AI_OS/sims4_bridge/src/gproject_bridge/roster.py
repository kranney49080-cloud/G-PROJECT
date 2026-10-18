"""Roster: name the active household's Sims after the real AIs, agents and tools.

Rules (from the project owner): every Sim is named after the real AI/agent/tool/skill it stands
for, no invented names, at most 8 on the lot. This module only RENAMES Sims that already exist in
the active household (SimInfo.first_name / last_name setters, verified in the game's scripts).
It never creates, moves or deletes Sims.

  gp.roster            dry run: show who would be renamed to what (changes nothing)
  gp.roster apply      do the renames (originals saved first in roster_backup.json)
  gp.roster undo       restore the original names from roster_backup.json

Names come from config/staff.json (the "staff" list, field "name"); which of them are on the lot
is bridge_config.json -> roster.on_duty (max 8). Python 3.7 only.
"""
import json
import os
import time

from gproject_bridge import config, paths
from gproject_bridge.log import log

MAX_ON_LOT = 8

DEFAULT_ROSTER = {
    "staff_file": "",   # "" = <state_dir>\..\config\staff.json
    "on_duty": ["Claude", "Codex", "ChatGPT", "Gemini", "Antigravity", "Planner", "Coder", "Tester"],
    "last_name": "",
}


def _cfg():
    cfg = dict(DEFAULT_ROSTER)
    cfg.update(config.load().get("roster") or {})
    return cfg


def _staff_names(cfg):
    path = cfg.get("staff_file") or os.path.join(
        os.path.dirname(config.load()["state_dir"].rstrip("\\/")), "config", "staff.json")
    with open(path, "r", encoding="utf-8-sig") as fh:
        data = json.load(fh)
    return set(e.get("name") for e in data.get("staff", []) if e.get("name")), path


def _backup_path():
    return os.path.join(paths.mod_home(), "roster_backup.json")


def _read_backup():
    try:
        with open(_backup_path(), "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def _write_backup(data):
    with open(_backup_path(), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def _household_infos():
    import services
    household = services.active_household()
    if household is None:
        return None
    return sorted(household.sim_info_gen(), key=lambda i: i.sim_id)


def _full(info):
    return ("%s %s" % (info.first_name, info.last_name)).strip()


def plan():
    """Returns (rows, notes). rows = [(sim_info, current name, new first name)]."""
    cfg = _cfg()
    notes = []
    known, path = _staff_names(cfg)
    wanted = list(cfg["on_duty"])[:MAX_ON_LOT]
    if len(cfg["on_duty"]) > MAX_ON_LOT:
        notes.append("on_duty has %d names; only the first %d are used (max on the lot)" % (
            len(cfg["on_duty"]), MAX_ON_LOT))
    for n in wanted:
        if n not in known:
            notes.append("%r is not in %s (check the spelling)" % (n, path))
    infos = _household_infos()
    if infos is None:
        return None, ["no active household (load a lot first)"]
    have = {}
    for i in infos:
        have.setdefault(str(i.first_name).strip().lower(), i)
    todo = [n for n in wanted if n.strip().lower() not in have]
    free = [i for i in infos if str(i.first_name).strip().lower() not in
            [w.strip().lower() for w in wanted]]
    rows = []
    for name in todo:
        if not free:
            notes.append("no spare Sim in the household for %r (household has %d Sims)" % (name, len(infos)))
            continue
        info = free.pop(0)
        rows.append((info, _full(info), name))
    if not rows and not notes:
        notes.append("nothing to do: all on-duty names are already on household Sims")
    return rows, notes


def show():
    rows, notes = plan()
    lines = []
    for info, cur, new in (rows or []):
        lines.append("%s  ->  %s" % (cur or "(unnamed)", new))
    lines.extend(notes)
    return lines


def apply():
    rows, notes = plan()
    if rows is None:
        return notes
    cfg = _cfg()
    backup = _read_backup()
    out = []
    for info, cur, new in rows:
        key = str(info.sim_id)
        if key not in backup:   # keep the ORIGINAL name, never overwrite it with an AI name
            backup[key] = [str(info.first_name), str(info.last_name), time.strftime("%Y-%m-%d %H:%M:%S")]
    _write_backup(backup)
    for info, cur, new in rows:
        info.first_name = new
        info.last_name = cfg["last_name"]
        log("roster: %s -> %s (sim_id %s)" % (cur, new, info.sim_id))
        out.append("%s -> %s" % (cur or "(unnamed)", new))
    return out + notes


def undo():
    backup = _read_backup()
    if not backup:
        return ["nothing to undo (no roster_backup.json entries)"]
    infos = _household_infos()
    if infos is None:
        return ["no active household (load a lot first)"]
    by_id = dict((str(i.sim_id), i) for i in infos)
    out = []
    for key in list(backup):
        info = by_id.get(key)
        if info is None:
            out.append("sim %s not in this household, kept in backup" % key)
            continue
        first, last = backup[key][0], backup[key][1]
        log("roster: restore %s -> %s %s" % (_full(info), first, last))
        info.first_name = first
        info.last_name = last
        out.append("restored %s" % (("%s %s" % (first, last)).strip() or key))
        del backup[key]
    _write_backup(backup)
    return out
