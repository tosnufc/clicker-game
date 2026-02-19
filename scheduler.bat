@echo off
title Scheduler - 24/7 Workflow Launcher
cd /d D:\dev\clicker-game

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

:: Tuesday = 2
if "%dow%"=="2" (
    if "%now%"=="19:04" (
        echo [%date% %time%] Launching claim_8-hrs_workflow...
        start "" claim_8-hrs_workflow.bat
        set "last_run=%now%"
    )
    if "%now%"=="19:07" (
        echo [%date% %time%] Launching claim_8-hrs_workflow...
        start "" claim_8-hrs_workflow.bat
        set "last_run=%now%"
    )
)

:wait
:: Wait 30 seconds before checking again
timeout /t 30 /nobreak >nul
goto loop
