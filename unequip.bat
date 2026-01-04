@echo off
if "%1"=="minimized" goto run
start /min "" "%~f0" minimized
exit

:run
cd /d D:\dev\clicker
call .venv\Scripts\activate.bat
python unequip.py
exit

