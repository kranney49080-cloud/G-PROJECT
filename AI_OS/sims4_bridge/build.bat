@echo off
setlocal
set "HERE=%~dp0"
if not exist "%HERE%tools\py37\python.exe" (
  echo Python 3.7 not set up. Run: powershell -ExecutionPolicy Bypass -File "%HERE%setup_py37.ps1"
  exit /b 1
)
"%HERE%tools\py37\python.exe" "%HERE%build_mod.py" "%HERE%."
exit /b %ERRORLEVEL%
