@echo off
title Scheduler - 24/7 Workflow Launcher
cd /d "%~dp0"

echo ==========================================
echo  Scheduler started at %date% %time%
echo  Running 24/7 - Close window to stop
echo ==========================================
echo.

set "last_run="

:loop
:: Get current day of week (Mon=1, Tue=2, ... Sun=7)
for /f %%d in ('powershell -nologo -noprofile -command "(Get-Date).DayOfWeek.value__"') do set dow=%%d

:: Get current time in HH:mm format
for /f %%t in ('powershell -nologo -noprofile -command "Get-Date -Format HH:mm"') do set now=%%t

:: Skip if already launched in this minute
if "%now%"=="%last_run%" goto wait

:: ####### Claim 8-hrs workflow 3 times a day #######
if "%now%"=="10:00" (
    echo [%date% %time%] Launching claim_8-hrs_workflow...
    start "" claim_8-hrs_workflow.bat
    set "last_run=%now%"
)
if "%now%"=="18:00" (
    echo [%date% %time%] Launching claim_8-hrs_workflow...
    start "" claim_8-hrs_workflow.bat
    set "last_run=%now%"
)
if "%now%"=="02:00" (
    echo [%date% %time%] Launching claim_8-hrs_workflow...
    start "" claim_8-hrs_workflow.bat
    set "last_run=%now%"
)
:: ##################################################

:: ####### Claim daily workflow once a day #######
if "%now%"=="10:10" (
    echo [%date% %time%] Launching claim_daily_workflow...
    start "" claim_daily_workflow.bat
    set "last_run=%now%"
)
:: ################################################

:: ####### Prime Recruitment 30 workflow - weekly schedule #######
REM Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
if "%dow%"=="1" if "%now%"=="02:15" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="1" if "%now%"=="22:15" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="2" if "%now%"=="14:15" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="10:20" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="18:15" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="06:15" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="02:15" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="16:15" (
    echo [%date% %time%] Launching prime_recruitment_30_workflow...
    start "" prime_recruitment_30_workflow.bat
    set "last_run=%now%"
)
:: ###############################################################

:: ####### Boomer workflow - weekly schedule #######
REM Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
if "%dow%"=="1" if "%now%"=="20:00" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="2" if "%now%"=="05:00" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="00:15" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="00:30" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="14:00" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="10:20" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="14:00" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="0" if "%now%"=="10:20" (
    echo [%date% %time%] Launching boomer_workflow...
    start "" boomer_workflow.bat
    set "last_run=%now%"
)
:: #################################################

:: ####### Auto Join workflow twice a day #######
if "%now%"=="11:59" (
    echo [%date% %time%] Launching auto_join_workflow...
    start "" auto_join_workflow.bat
    set "last_run=%now%"
)
if "%now%"=="23:59" (
    echo [%date% %time%] Launching auto_join_workflow...
    start "" auto_join_workflow.bat
    set "last_run=%now%"
)
:: ##############################################

:: ####### Soldiers Popping workflow - weekly schedule #######
REM Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
if "%dow%"=="2" if "%now%"=="03:30" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="2" if "%now%"=="23:30" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="3" if "%now%"=="15:30" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="4" if "%now%"=="10:55" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="5" if "%now%"=="20:30" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="6" if "%now%"=="07:30" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="0" if "%now%"=="03:30" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
if "%dow%"=="0" if "%now%"=="20:30" (
    echo [%date% %time%] Launching soldiers_popping_workflow...
    start "" soldiers_popping_workflow.bat
    set "last_run=%now%"
)
:: ###########################################################

:wait
:: Wait 30 seconds before checking again
timeout /t 30 /nobreak >nul
goto loop
