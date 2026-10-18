@echo off
cd /d "%~dp0"
echo KEY 3 of 3 - ADMIN (broad) token: checks the key and shows what it sees. Read only.
set "PYX="
where py >nul 2>nul && set "PYX=py -3"
if not defined PYX where python >nul 2>nul && set "PYX=python"
if not defined PYX ( echo Python was not found. Tell Claude this exact line. & pause & exit /b 1 )
%PYX% af_admin.py
echo.
echo Exit code: %errorlevel%
pause
