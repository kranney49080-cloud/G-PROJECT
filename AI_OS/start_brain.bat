@echo off
rem Starts the Agentic 3D brain in the background (minimised, low priority).
rem Reads API keys from your Windows user environment at launch, because a program
rem started from Explorer does not see variables saved after Explorer started.
rem The keys are only copied into this process; nothing is written to disk.
for %%K in (GROQ_API_KEY OPENROUTER_API_KEY DEEPSEEK_API_KEY) do (
  for /f "tokens=2,*" %%a in ('reg query "HKCU\Environment" /v %%K 2^>nul ^| findstr /b /c:"    %%K"') do set "%%K=%%b"
)
cd /d F:\MrMak\Workspace
start "Agentic 3D brain" /min /low py -3 scripts\ai_os.py serve
