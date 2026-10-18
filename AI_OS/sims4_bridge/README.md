# Agentic 3D Sims 4 Bridge (the Screen)

Stage (a): build chain + load proof. No polling, menus or popups yet.

## One-time setup
1. `powershell -ExecutionPolicy Bypass -File setup_py37.ps1`  (isolated Python 3.7.0 in tools\py37, nothing system-wide)
2. `build.bat`  -> dist\GProjectBridge.ts4script + dist\bridge_config.json

## Install into the game
1. Copy BOTH dist files into a subfolder of your Sims 4 Mods folder, e.g. `Mods\GProject\` (script mods work at most 1-2 folders deep; keep it shallow).
2. In-game: Game Options > Other > enable "Script Mods Allowed", restart the game.
3. Check `Mods\GProject\gproject_bridge.log` for "Agentic 3D bridge ... loaded". That line is the stage (a) pass.

## Notes
- The game runs Python 3.7.0; the build requires Python 3.7.x (same bytecode format) and refuses anything else.
- Polling target lives in bridge_config.json (state_dir), per blueprint s4.
