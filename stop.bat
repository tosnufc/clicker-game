@echo off
REM Batch script to force stop all Python/PowerShell/CMD processes started
REM by .py/.ps1/.bat files in this directory (mirrors stop.ps1 behavior).

setlocal EnableDelayedExpansion

REM If not relaunched hidden, re-run this script in a hidden window via mshta
if /I not "%~1"=="hidden" (
    mshta vbscript:createobject("wscript.shell").run("""%~f0"" hidden",0,true)(window.close)
    exit /b
)

set "scriptDir=%~dp0"
if "%scriptDir:~-1%"=="\" set "scriptDir=%scriptDir:~0,-1%"

echo Stopping all automation processes from %scriptDir%...
echo.

call :killByPattern "python.exe" "py" "Python"
echo.
call :killByPattern "powershell.exe" "ps1" "PowerShell"
echo.
call :killByPattern "cmd.exe" "bat" "CMD"

echo.
echo All automation processes have been terminated.
endlocal
exit /b

REM ---------------------------------------------------------------------------
REM :killByPattern <processName> <extension> <label>
REM   Kills every <processName> whose command line references any *.<extension>
REM   file in this script's directory (skipping stop.ps1 / stop.bat).
REM ---------------------------------------------------------------------------
:killByPattern
set "procName=%~1"
set "ext=%~2"
set "label=%~3"
set "found=0"

REM Enumerate matching files, but skip this script and its PS counterpart
for %%F in ("%scriptDir%\*.%ext%") do (
    if /I not "%%~nxF"=="stop.ps1" if /I not "%%~nxF"=="stop.bat" (
        REM WMIC query: name='<proc>' AND commandline LIKE '%<file>%'
        REM Outer for /f reads raw lines; inner for /f re-tokenizes to strip
        REM the stray CR that wmic appends (\r\r\n line endings) and to
        REM discard non-numeric lines (header, "No Instance(s) Available.").
        for /f "usebackq skip=1 delims=" %%L in (`wmic process where "name='%procName%' and commandline like '%%%%~nxF%%'" get processid 2^>nul`) do (
            for /f "tokens=1" %%P in ("%%L") do (
                set "pidVal=%%P"
                echo !pidVal!| findstr /r "^[0-9][0-9]*$" >nul && (
                    echo Stopping %label% process ^(PID: !pidVal!^) - %%~nxF
                    taskkill /F /PID !pidVal! >nul 2>&1
                    set "found=1"
                )
            )
        )
    )
)

if "!found!"=="0" (
    echo No %label% processes found.
) else (
    echo %label% processes stopped.
)
exit /b
