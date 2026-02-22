@echo off
if "%1"=="minimized" goto run
start /min "" "%~f0" minimized
exit

:run
cd /d "%~dp0"
call .venv\Scripts\activate.bat

echo Muting volume...
python mute.py

echo Step 1: Login
python login.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 2: Clear Login Adds
python clear_login_adds.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 3: Claim Daily
python claim_daily.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 4: Claim Blueprints
python claim_blueprints.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 5: Logout
python logout.py

echo Restoring volume...
python unmute.py

exit
