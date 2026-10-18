@echo off
set "EXE=F:\Downloads\actrun-v0.16.11.cli-x64-windows\actrun.exe"
set "ACT=F:\Downloads\actrun-v0.16.11.cli-x64-windows\hello-world.act"
set "LOG=F:\MrMak\Workspace\AI_OS\state\hello_world.log"
echo TEST: running actrun hello-world.act (only prints text, changes nothing)
if not exist "%EXE%" ( echo actrun.exe not found at %EXE% & pause & exit /b 1 )
"%EXE%" "%ACT%" > "%LOG%" 2>&1
echo Exit code: %errorlevel% >> "%LOG%"
type "%LOG%"
echo.
echo (Output also saved to %LOG%)
pause
