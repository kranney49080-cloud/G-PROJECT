@echo off
cd /d "%~dp0"
echo Starting talk listener. Leave this window open. Close it to stop.
echo PC addresses (use the 192.168.x.x one on your phone):
ipconfig | findstr /i "IPv4"
echo.
py -3 talk_listener.py
pause
