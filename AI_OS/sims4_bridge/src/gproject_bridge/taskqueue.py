"""Stage (c) engine: submit a task to the brain's queue (blueprint section 5A).

One file per task in queue/tasks/, written atomically: the JSON goes to a temp
file in the PARENT queue folder (so the brain's file watcher never sees a
half-written file) and is then moved into tasks/ with os.replace.
The Sims pie menu and the cheat-console command both call submit().
"""
import json
import os
import time

from gproject_bridge import config, poller
from gproject_bridge.log import log

MAX_PROMPT_CHARS = 2000
_counter = 0


def _identity(cfg, sim_name=""):
    """Pick the Sim id / role: the clicked Sim's name if mapped, else config, else the HUD's."""
    mapped = (cfg.get("sim_map") or {}).get(str(sim_name).strip().lower())
    if isinstance(mapped, dict):
        return str(mapped.get("sim_id", "0413")), str(mapped.get("role", "coder")).lower()
    cur = poller.current or {}
    sim_id = str(cfg.get("default_sim_id") or cur.get("sim_id") or "0413")
    role = str(cfg.get("default_role") or cur.get("assigned_role") or "coder").lower()
    return sim_id, role


def build_task(prompt, cfg=None, sim_name=""):
    """Pure function: prompt -> (task_id, task dict) per the 5A contract."""
    global _counter
    cfg = cfg or config.load()
    prompt = " ".join(str(prompt).split())
    if not prompt:
        raise ValueError("empty prompt")
    if len(prompt) > MAX_PROMPT_CHARS:
        prompt = prompt[:MAX_PROMPT_CHARS]
    _counter += 1
    task_id = "T-SIM-%s-%d" % (time.strftime("%Y%m%d%H%M%S"), _counter)
    sim_id, role = _identity(cfg, sim_name)
    return task_id, {
        "task_id": task_id,
        "assigned_sim_id": sim_id,
        "sim_role": role,
        "prompt": prompt,
        "preferred_tier": cfg.get("preferred_tier", "auto"),
    }


def submit(prompt, sim_name=""):
    """Write one task file. Returns the task_id. Raises on failure (callers catch)."""
    cfg = config.load()
    task_id, task = build_task(prompt, cfg, sim_name)
    tasks_dir = cfg["queue_tasks_dir"]
    os.makedirs(tasks_dir, exist_ok=True)
    staging = os.path.join(os.path.dirname(os.path.normpath(tasks_dir)), ".tmp-" + task_id + ".json")
    final = os.path.join(tasks_dir, task_id + ".json")
    with open(staging, "w", encoding="utf-8") as fh:
        json.dump(task, fh, indent=2)
    os.replace(staging, final)
    log("queue: submitted %s (%d chars)" % (task_id, len(task["prompt"])))
    return task_id


def _last_task_id():
    import re
    cur = poller.current or {}
    for key in ("task_id", "task_description", "current_task", "description"):
        m = re.search(r"T-[A-Za-z0-9_-]+", str(cur.get(key) or ""))
        if m:
            return m.group(0)
    m = re.search(r"T-[A-Za-z0-9_-]+", json.dumps(cur))
    return m.group(0) if m else None


def submit_rating(scores):
    """Write queue/ratings/<task>.json with 0-5 scores per category. Returns the task id."""
    task_id = _last_task_id()
    if not task_id:
        raise ValueError("no finished task on the HUD yet")
    cfg = config.load()
    rdir = os.path.join(os.path.dirname(os.path.normpath(cfg["queue_tasks_dir"])), "ratings")
    os.makedirs(rdir, exist_ok=True)
    name = "%s-%s.json" % (task_id, time.strftime("%H%M%S"))
    tmp = os.path.join(rdir, ".tmp-" + name)
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"task_id": task_id, "scores": scores}, fh, indent=2)
    os.replace(tmp, os.path.join(rdir, name))
    log("rating: %s %s" % (task_id, scores))
    return task_id
