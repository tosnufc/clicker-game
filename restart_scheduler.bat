@echo off
for /L %%i in (60,1,64) do (
    echo === Restart scheduler on 192.168.1.%%i ===
    "C:\Program Files\Git\usr\bin\ssh.exe" user@192.168.1.%%i "d: && cd dev\clicker-game && .venv\Scripts\python.exe close_game_dialog.py && .venv\Scripts\python.exe scheduler_restart.py && exit"
    echo.
)
pause
