@echo off
cd /d "%~dp0"
REM start = return immediately so cmd.exe does not stay open on top of the screen
start "" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0screenshot.py" %*
