@echo off
for /L %%i in (60,1,64) do (
    echo === git pull on 192.168.1.%%i ===
    "C:\Program Files\Git\usr\bin\ssh.exe" user@192.168.1.%%i "d: && cd dev\clicker-game && git pull && exit"
    echo.
)
pause
