@echo off
title Scheduler - 24/7 Workflow Launcher
cd /d "%~dp0"

:: Get last octet of IPv4 address for log file name (one-time at startup)
set "last_octet=0"
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4" 2^>nul') do (
    for /f "tokens=4 delims=." %%b in ("%%a") do set "last_octet=%%b"
)
set "logfile=%~dp0%last_octet%_scheduler.log"

call :log "Scheduler started"

echo ==========================================
echo  Scheduler started at %date% %time%
echo  Log file: %logfile%
echo  Running 24/7 - Close window to stop
echo ==========================================
echo.

set "last_run="

:loop
:: Get current day of week (Sun=0, Mon=1, ... Sat=6) - lightweight WMIC instead of PowerShell
for /f "tokens=2 delims==" %%d in ('wmic path win32_localtime get dayofweek /value 2^>nul') do for /f "tokens=*" %%x in ("%%d") do set "dow=%%x"

:: Get current time in HH:mm format - pure batch, no process spawned
set "now=%time:~0,5%"
if "%now:~0,1%"==" " set "now=0%now:~1%"

:: Skip if already launched in this minute
if "%now%"=="%last_run%" goto wait

:: ####### Claim 8-hrs workflow 3 times a day #######
if "%now%"=="10:00" (
    call :log "Launching claim_8-hrs_workflow..."
    start "" claim_8-hrs_workflow.bat
    set "last_run=%now%"
)
if "%now%"=="18:00" (
    call :log "Launching claim_8-hrs_workflow..."
    start "" claim_8-hrs_workflow.bat
    set "last_run=%now%"
)
if "%now%"=="02:00" (
    call :log "Launching claim_8-hrs_workflow..."
    start "" claim_8-hrs_workflow.bat
    set "last_run=%now%"
)
:: ##################################################

:: ####### Claim daily workflow once a day #######
if "%now%"=="10:10" (
    call :log "Launching claim_daily_workflow..."
    start "" claim_daily_workflow.bat
    set "last_run=%now%"
)
:: ################################################

:: ####### Prime Recruitment 30 workflow - weekly schedule #######
REM Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
if "%dow%"=="1" if "%now%"=="02:15" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="1" if "%now%"=="22:15" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="2" if "%now%"=="14:15" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="10:20" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="18:15" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="06:15" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="02:15" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="16:15" (
    call :log "Launching prime_recruitment_30_workflow..."
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
:: ###############################################################

:: ####### Boomer workflow - weekly schedule #######
REM Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
if "%dow%"=="1" if "%now%"=="20:00" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="2" if "%now%"=="05:00" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="00:15" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="00:30" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="14:00" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="10:20" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="14:00" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="0" if "%now%"=="10:20" (
    call :log "Launching boomer_workflow..."
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
:: #################################################

:: ####### Auto Join workflow twice a day #######
if "%now%"=="11:59" (
    call :log "Launching auto_join_workflow..."
    start "" auto_join_workflow.bat
    set "last_run=%now%"
)
if "%now%"=="23:59" (
    call :log "Launching auto_join_workflow..."
    start "" auto_join_workflow.bat
    set "last_run=%now%"
)
:: ##############################################

:: ####### Soldiers Popping workflow - weekly schedule #######
REM Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
if "%dow%"=="2" if "%now%"=="03:30" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="2" if "%now%"=="23:30" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="15:30" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="10:55" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="20:30" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="07:30" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="0" if "%now%"=="03:30" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="0" if "%now%"=="20:30" (
    call :log "Launching soldiers_popping_workflow..."
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
:: ###########################################################

:: ####### Soldiers Training workflow - 13hrs before each popping #######
REM Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
if "%dow%"=="1" if "%now%"=="14:30" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="2" if "%now%"=="10:30" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="02:30" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="22:55" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="07:30" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="20:45" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="14:55" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="0" if "%now%"=="07:30" (
    call :log "Launching soldiers_training_workflow..."
    start "" soldiers_training_workflow.bat
    set "last_run=%now%"
)
:: ######################################################################

:wait
:: Wait 30 seconds before checking again
timeout /t 30 /nobreak >nul
goto loop

:log
echo [%date% %time%] %~1
echo [%date% %time%] %~1 >> "%logfile%" 2>nul
goto :eof
