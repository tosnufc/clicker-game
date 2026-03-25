@echo off
for /L %%i in (60,1,64) do (
    echo === git pull on 192.168.1.%%i ===
    "C:\Program Files\Git\usr\bin\ssh.exe" user@192.168.1.%%i "d: && cd dev\clicker-game && git pull && exit"
    echo.
)
rem Skip pause when run non-interactively (e.g. from scheduler_server after save)
if "%~1"=="" pause
