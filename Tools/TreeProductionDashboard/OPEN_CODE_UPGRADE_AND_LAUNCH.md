# OpenCode Work Order — Tree Production Dashboard V3

## Goal
Upgrade the existing Tree Production Dashboard into the main control panel for Tree 01.

Keep the current cozy dark-teal forest look, but make the dashboard substantially more useful for production.

Repository: `kranney49080-cloud/G-PROJECT`
Dashboard: `Tools/TreeProductionDashboard/`
Manifest: `Tools/TreeProductionDashboard/tree_01_manifest.json`

## Required features

### Project status
Show whether the dashboard is connected to the local project or running in local-only mode. Also show current branch, unsaved changes, uncommitted manifest changes, and last successful project save/push.

### Tree 01 manifest
Treat `tree_01_manifest.json` as the source of truth for Tree 01. Preserve existing useful data and extend the schema as needed.

Track at least:
- Tree 01 status
- last updated time
- master reference path
- palette specification path
- palette statistics path
- height
- trunk width
- canopy width
- root radius
- cut height
- texture resolution
- target card count
- poly budget
- notes
- approval history

### Asset cards
Create cards for:
- Standing Hero Tree
- Oblique / Side View
- Felled Tree
- Stump
- Cut Surface
- Local Canopy
- Shared Canopy
- Harvested Logs
- Chop Damage Marks

Each card should support:
- real image preview from a project-relative path
- status
- version
- approval state
- approval notes
- dependencies
- revision notes

If no image is assigned, show a clean placeholder.

### Large asset inspector
Clicking an asset card should open a larger inspector with the image, version, status, approval state, notes, dependencies, and buttons for **Approve** and **Needs Revision**.

Each approval/revision action must append a timestamped entry to approval history rather than deleting old history.

### Master reference panel
Show:
- master reference image/path
- palette spec path
- palette stats path
- color rule: `blue-black → dark teal → slate teal → blue-grey → pale cyan-grey`
- reminder that warm brown is an undertone, not the dominant bark color

### Tree specifications
Add editable fields for:
- height
- trunk width
- canopy width
- root radius
- cut height
- texture resolution
- target card count
- poly budget
- notes

### Harvesting states
Display this sequence visually:

`Standing → Damaged → Falling → Stump + Logs → Regrowth`

Show readiness for each state.

### Canopy ownership
Clearly distinguish:
- **Tree-local canopy** — disappears/fades with the harvested tree
- **Shared forest canopy** — remains when a single tree is harvested

Use 20–30% local canopy and 70–80% shared canopy as editable starting targets, not hard rules.

### Dependencies
Default behavior:
- Standing Tree approval unlocks Oblique, Felled, Stump, and Cut Surface for production.
- Local Canopy stays locked until the standing structure is approved.
- Shared Canopy is later-stage work and should not block the first harvesting prototype.
- Manual override is allowed, but show a warning.

### Unreal verification
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

### Save controls
Keep three clear actions:
- **Save Locally**
- **Save to Project**
- **Save & Push to GitHub**

Do not include unrelated project files in dashboard saves or pushes.

## Local companion server
Create `server.py` if needed so the dashboard can safely read/write the project manifest from the local repository.

Requirements:
- local machine only
- use `127.0.0.1`
- default to port `8765` and use another free local port if necessary
- serve the dashboard
- read/write the Tree 01 manifest
- expose only the small API needed by the dashboard
- print the local dashboard URL clearly in the console

## Local-only fallback
Opening `index.html` directly should still work.

In local-only mode:
- render the dashboard normally
- use localStorage
- display **Local-only mode**
- disable project-save/push controls
- avoid repeated errors

## Launcher
Create:
- `launch_dashboard.ps1`
- `launch_dashboard.bat`

The launcher should:
1. find the dashboard folder
2. locate Python using `py` first, then `python`
3. start the local server
4. wait until it is ready
5. print the dashboard URL clearly
6. keep the console available for status/errors
7. explain how to stop the server

### Important
**Do not automatically open or launch the user's browser.**

The user will open the printed URL manually.

## Verification before stopping
Test and report:
1. launcher starts the server without opening a browser
2. console prints a valid local URL
3. dashboard loads without JavaScript errors when opened manually
4. project status endpoint works
5. manifest loading works
6. Save to Project persists edits
7. refresh reloads saved values
8. approvals append history
9. valid image paths show previews
10. local-only mode works
11. project push does not include unrelated files
12. report a commit hash if one is created
13. state clearly if anything could not be tested

## Final report
When finished, report:
- files created
- files modified
- tests and results
- dependencies introduced
- exact local dashboard URL
- commit hash if applicable
- anything incomplete

Implement and test the work. Do not just describe it.

**Do not auto-launch the browser.**
