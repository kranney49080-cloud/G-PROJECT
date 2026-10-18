@echo off
cd /d "%~dp0"
echo KEY 2 of 3 - AGENT token: connects this PC as a job runner. Close this window to stop.
set "PYX="
where py >nul 2>nul && set "PYX=py -3"
if not defined PYX where python >nul 2>nul && set "PYX=python"
if not defined PYX ( echo Python was not found. Tell Claude this exact line. & pause & exit /b 1 )
%PYX% af_agent.py
echo.
echo Exit code: %errorlevel%
pause
