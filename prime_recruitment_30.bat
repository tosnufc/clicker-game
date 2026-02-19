@echo off
if "%1"=="minimized" goto run
start /min "" "%~f0" minimized
exit

:run
cd /d D:\dev\clicker-game
call .venv\Scripts\activate.bat
python prime_recruitment_30.py
exit
