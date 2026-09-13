# OpenCode Work Order — Tree Production Dashboard V3

## Objective
Upgrade the existing Tree Production Dashboard into a practical local project tool that:

1. loads Tree 01 state from the repository manifest;
2. saves approvals, notes, image paths, versions, harvest states, dependencies, and Unreal verification back into the repository manifest;
3. can safely commit and push only the dashboard/manifest changes to GitHub using the user's existing local Git credentials;
4. launches itself in the user's browser with one click;
5. preserves the current cozy dark forest visual design;
6. does not require Astra credits or any paid service.

Repository: `kranney49080-cloud/G-PROJECT`
Dashboard folder: `Tools/TreeProductionDashboard/`
Existing manifest: `Tools/TreeProductionDashboard/tree_01_manifest.json`

---

## Non-negotiable safety rules

- Inspect the existing dashboard files and manifest before editing.
- Do not delete or rewrite unrelated project files.
- Do not use `git add .` or stage unrelated files.
- Never force-push.
- Never store a GitHub token, password, credential, or secret in HTML, JavaScript, JSON, source code, localStorage, or the repository.
- Use the user's existing local Git authentication / Git Credential Manager for push operations.
- If the repository has unrelated uncommitted changes, do not include them in the dashboard commit.
- If Git cannot push safely, show a clear UI error instead of trying destructive recovery.
- Preserve all current dashboard functionality unless it is superseded by a better implementation.
- Keep the dashboard usable in local-only mode if GitHub is unavailable.

---

# Architecture

Implement a tiny local companion server rather than putting GitHub credentials in the browser.

Preferred implementation: Python standard library only, if practical.

Create:

`Tools/TreeProductionDashboard/server.py`

The server should:

- serve the dashboard files locally;
- bind to `127.0.0.1` only;
- default to port `8765` and find the next free port if necessary;
- read/write `tree_01_manifest.json` on disk;
- expose a very small API to the dashboard;
- optionally run safe Git commands for a deliberate Save & Push action;
- open the browser automatically when started with the launcher.

Do not create a public network service.

---

# Required local API

Implement equivalent endpoints to these names unless there is a strong technical reason to rename them.

## `GET /api/status`
Return JSON with at least:

- `connected: true`
- current repository branch
- repository root path
- manifest path
- whether the working tree contains unrelated changes
- whether the manifest has unsaved/uncommitted changes
- latest commit hash if available

## `GET /api/manifest`
Read and return the current `tree_01_manifest.json` from the repository.

## `POST /api/manifest`
Validate and atomically save the submitted manifest to `tree_01_manifest.json`.

Requirements:

- write to a temporary file first, then replace;
- reject malformed JSON;
- preserve a useful schema;
- add/update a `lastUpdated` timestamp;
- do not commit automatically.

## `POST /api/commit-push`
This action must only occur after the user explicitly presses a button such as **Save & Push**.

Behavior:

1. save/validate manifest first;
2. determine current branch;
3. stage only explicitly permitted dashboard files, preferably only `Tools/TreeProductionDashboard/tree_01_manifest.json` unless dashboard source files themselves were intentionally edited;
4. create a commit such as `Update Tree 01 production manifest`;
5. push the current branch normally;
6. never use force push;
7. return success/failure, commit hash, and human-readable error text.

If there are unrelated changes in the repository, they must remain untouched and unstaged.

---

# Manifest

Treat `tree_01_manifest.json` as the source of truth for Tree 01.

If fields are missing, extend the manifest in a backwards-compatible way. It should be able to represent at least:

```json
{
  "id": "tree_01",
  "name": "Tree 01",
  "status": "in-progress",
  "lastUpdated": "ISO_TIMESTAMP",
  "masterReference": {
    "path": "",
    "paletteSpec": "Art/Environment/Trees/Master_Reference/FOREST_TREE_MASTER_COLOR_SPEC.md",
    "paletteStats": "Art/Environment/Trees/Master_Reference/FOREST_TREE_MASTER_COLOR_STATS.csv"
  },
  "specs": {
    "heightFeet": 50,
    "trunkWidthFeet": null,
    "canopyWidthFeet": null,
    "cutHeightFeet": null,
    "notes": ""
  },
  "assets": {
    "standing": {},
    "oblique": {},
    "felled": {},
    "stump": {},
    "cutSurface": {},
    "localCanopy": {},
    "sharedCanopy": {},
    "logs": {},
    "damageMarks": {}
  },
  "harvestStates": {},
  "unrealVerification": {},
  "approvalHistory": []
}
```

Each asset should be able to store:

- status;
- current version;
- image path;
- approval state;
- approval notes;
- dependencies;
- optional dimensions/specification data.

Do not overwrite existing useful manifest data while extending it.

---

# Dashboard V3 UI requirements

Preserve the current dark teal / cozy forest look.

Add the following.

## 1. Project connection header
At the top show:

- **Project connected** / **Local-only mode**
- branch name
- unsaved indicator
- uncommitted indicator
- last successful GitHub push

## 2. Actual asset image previews
Each asset card should support a project-relative image path and display the actual image when available.

Cards:

- Standing Hero Tree
- Oblique / Side View
- Felled Tree
- Stump
- Cut Surface
- Local Canopy
- Shared Canopy
- Harvested Logs
- Chop Damage Marks

If no image exists, show an attractive placeholder rather than a broken-image icon.

## 3. Large asset inspector
Clicking a card should open a larger inspector/modal with:

- large image preview;
- version number;
- status;
- approval state;
- image path;
- revision notes;
- dependencies;
- Approve button;
- Needs Revision button.

## 4. Master Reference panel
Add a permanent reference section showing:

- master reference path/image if available;
- palette-spec link/path;
- palette-stats link/path;
- core color rule: `blue-black → dark teal → slate teal → blue-grey → pale cyan-grey`;
- reminder: warm brown is an undertone, not the dominant bark color.

Do not duplicate the entire statistical file into the UI; link/read the project files instead where practical.

## 5. Tree specifications
Editable fields for:

- height;
- trunk width;
- canopy width;
- root radius;
- cut height;
- intended texture resolution;
- target card count;
- target geometry/poly budget if used;
- freeform notes.

## 6. Harvest state preview
Display the sequence visually:

`Standing → Damaged → Falling → Stump + Logs → Regrowth`

Each state should indicate whether the required asset/mechanic is ready.

## 7. Canopy ownership panel
Clearly distinguish:

- **Tree-local canopy** — disappears/fades with this tree;
- **Shared forest canopy** — remains when one tree is harvested.

Show the current design targets of roughly 20–30% local canopy and 70–80% shared canopy as editable targets, not hard rules.

## 8. Dependencies and locks
Default production dependency behavior:

- Standing Tree must be approved before Oblique, Felled, Stump, and Cut Surface are treated as production-ready.
- Local Canopy remains locked until the standing structure is approved.
- Shared Forest Canopy is later-stage work and should not block the first harvest-loop prototype.
- Unreal final verification should remain incomplete until the core asset set is ready.

Allow manual override, but warn before overriding a dependency.

## 9. Unreal verification panel
Track:

- Imported
- Scale correct
- Material correct
- Collision correct
- Harvest interaction works
- Falling state works
- Local canopy removal works
- Stump/resource state works
- Performance checked

## 10. Version / approval history
Every approval or Needs Revision action should append a small entry to `approvalHistory` with:

- timestamp;
- asset ID;
- version;
- action;
- note.

Do not delete earlier history when a new version is added.

## 11. Save controls
Provide three visibly different actions:

### Save Locally
Browser/local fallback only.

### Save to Project
POST to `/api/manifest` and save the repo manifest without committing.

### Save & Push to GitHub
POST to `/api/commit-push` only after a confirmation dialog showing exactly which file(s) will be committed.

Show success/failure clearly.

---

# Launcher / "pop it up" requirement

Create:

- `launch_dashboard.ps1`
- `launch_dashboard.bat`

## Windows behavior
Double-clicking `launch_dashboard.bat` should:

1. locate the dashboard folder relative to the script;
2. locate Python using `py` first, then `python`;
3. start `server.py`;
4. wait until the server responds;
5. automatically open the dashboard URL in the user's default browser;
6. keep a small console window available for server/error messages;
7. print a clear message explaining how to stop the server.

The PowerShell script can perform the actual logic, with the BAT file serving as the easy double-click entry point.

If Python cannot be found, display a clear message and pause rather than silently failing.

Do not require administrator privileges.

---

# Local-only fallback

If the user opens `index.html` directly without `server.py`:

- the dashboard should still render;
- localStorage functionality should still work;
- clearly display **Local-only mode**;
- disable or hide Save to Project / Save & Push;
- do not throw repeated console/network errors.

---

# Verification checklist — OpenCode must complete before stopping

OpenCode must test and report evidence for all of the following:

1. `launch_dashboard.bat` opens the dashboard in a browser.
2. Dashboard loads without JavaScript errors.
3. `GET /api/status` works.
4. `GET /api/manifest` reads the repository manifest.
5. Editing notes/specs and pressing Save to Project changes `tree_01_manifest.json`.
6. Refreshing the page reloads the saved manifest values.
7. Asset approval appends approval history.
8. Image-path field shows a preview when given a valid local project image.
9. Local-only mode still works when `index.html` is opened directly.
10. Save & Push stages no unrelated project files.
11. If push is tested, report the exact commit hash.
12. If push cannot be tested safely, do not fake success; state the exact reason.

---

# Final response required from OpenCode

When finished, provide a short report containing:

- files created;
- files modified;
- tests run and their results;
- any dependencies introduced;
- exact URL opened locally;
- exact Git commit hash if a commit was made;
- anything still incomplete.

Then **launch the dashboard automatically** so the user sees it immediately.

Do not merely describe how to implement this. Implement it, test it, and open it.
