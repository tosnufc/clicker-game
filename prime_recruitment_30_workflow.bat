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
echo Waiting 90 seconds...
timeout /t 90 /nobreak >nul

echo Step 2: Clear Login Adds
python clear_login_adds.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 3: Prime Recruitment 30
python prime_recruitment_30.py
echo Waiting 30 seconds...
timeout /t 30 /nobreak >nul

echo Step 4: Logout
python logout.py

echo Restoring volume...
python unmute.py

exit
