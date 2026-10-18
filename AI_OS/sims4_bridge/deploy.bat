@echo off
rem Build the mod and copy it into the Sims 4 Mods folder (one command).
rem Override the target with:  set GP_MODS_DIR=C:\path\to\Mods\GProject
setlocal
set "HERE=%~dp0"
call "%HERE%build.bat" || exit /b 1
if "%GP_MODS_DIR%"=="" set "GP_MODS_DIR=%USERPROFILE%\OneDrive\Documents\Electronic Arts\The Sims 4\Mods\GProject"
if not exist "%GP_MODS_DIR%" mkdir "%GP_MODS_DIR%"
copy /Y "%HERE%dist\GProjectBridge.ts4script" "%GP_MODS_DIR%\" >nul || exit /b 1
if not exist "%GP_MODS_DIR%\bridge_config.json" copy "%HERE%dist\bridge_config.json" "%GP_MODS_DIR%\" >nul
echo DEPLOYED: %GP_MODS_DIR%
exit /b 0
