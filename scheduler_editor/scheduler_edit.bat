@echo off
cd /d "%~dp0"
call ..\.venv\Scripts\activate.bat
echo Press Enter in this window (or click Exit in the browser) to stop.
start http://127.0.0.1:8765/scheduler.html
python scheduler_server.py
