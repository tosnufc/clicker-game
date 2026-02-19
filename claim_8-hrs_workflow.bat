@echo off
if "%1"=="minimized" goto run
start /min "" "%~f0" minimized
exit

:run
cd /d D:\dev\clicker-game
call .venv\Scripts\activate.bat

echo Muting volume...
python mute.py

echo Step 1: Login
python login.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 2: Claim 20
python claim_8-hrs.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 3: Logout
python logout.py

echo Restoring volume...
python unmute.py

exit
