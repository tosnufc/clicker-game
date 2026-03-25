@echo off
title Restart scheduler (remotes)
cd /d "%~dp0"

REM Use "&" between Python steps so scheduler_restart always runs even if close_game_dialog fails.
REM (Old "&&" skipped restart when the first script returned non-zero.)
for /L %%i in (60,1,64) do (
    echo === Restart scheduler on 192.168.1.%%i ===
    "C:\Program Files\Git\usr\bin\ssh.exe" user@192.168.1.%%i "d: && cd dev\clicker-game && .venv\Scripts\python.exe close_game_dialog.py & .venv\Scripts\python.exe scheduler_restart.py && exit"
    echo.
)
rem Skip pause when run non-interactively (e.g. from scheduler_server after Save)
if "%~1"=="" pause
