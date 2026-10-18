# Naming note: "Agentic 3D" vs "G-Project" / "gproject"

The project is now called **Agentic 3D** (renamed 2026-10-13). Everything a person reads or sees uses the new name: in-game menus, dialogs and popups, the brain window title, the blueprint, the brain config and the bridge README.

Some internal identifiers still say `gproject` / `GProject` on purpose. They are never shown to the user, and renaming them means rebuilding the Sims 4 mod and moving its folder, which could silently break the in-game menus:

| Old name still in use | Where | Why it stays |
|---|---|---|
| `gproject_bridge` | Python module inside `GProjectBridge.ts4script`; the tuning XML `m="gproject_bridge.ask_interaction"` points at it | Renaming requires rebuilding the script and every tuning package together |
| `GProject_AskBig`, `GProject_RateTask`, `GProject_AskBrain`, `GProject_WriteRequest`, `GProject_SendRequest` | Interaction tuning names (IDs are hashes of these names) | Changing a name changes its ID |
| `Mods\GProject\` | Sims 4 Mods subfolder | Contains the live mod files |
| `GProjectBridge.ts4script`, `GProjectAskBrain.package`, `GProjectBigBox.package`, `GProjectAskLong.package` | Mod files | Same as above |
| `gproject_bridge.log` | Mod log file | Tools read it by this name |
| `GP_` prefix | Environment variable `GP_MODS_DIR`, string keys | Internal only |

If you ever do the full rename, do it in one pass: rebuild the script and packages with the new module and tuning names, delete the old files from the Mods folder, restart the game, and check `lastException.txt` for errors.

Backups of every file changed by the rename sit next to the originals as `*.pre-rename.bak`.
