@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
echo Building the Sims 4 mod (build only, nothing is installed)...
(
  echo === %date% %time%
  if not exist "tools\py37\python.exe" (
    echo ERROR: tools\py37\python.exe not found
  ) else (
    "tools\py37\python.exe" build_mod.py "%~dp0."
  )
  echo EXIT CODE: !errorlevel!
) > build_log.txt 2>&1
type build_log.txt
echo.
echo The same text is saved in build_log.txt in this folder.
pause
