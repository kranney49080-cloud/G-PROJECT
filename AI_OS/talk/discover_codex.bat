@echo off
cd /d "%~dp0"
echo Codex activity test, 60 seconds.
set "PYX="
where py >nul 2>nul && set "PYX=py -3"
if not defined PYX where python >nul 2>nul && set "PYX=python"
if not defined PYX ( echo Python was not found. Tell Claude this exact line. & pause & exit /b 1 )
%PYX% codex_watcher.py --discover
echo.
echo Exit code: %errorlevel%
pause
