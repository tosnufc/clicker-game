# PowerShell script to force stop all Python processes started by .py files in this directory

param([switch]$Hidden)

# If not running hidden, relaunch the script hidden
if (-not $Hidden) {
    Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$PSCommandPath`" -Hidden" -WindowStyle Hidden
    exit
}

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $PSCommandPath

# Get all .py files in the directory and build a regex pattern
$pyFiles = Get-ChildItem -Path $scriptDir -Filter "*.py" | ForEach-Object { [regex]::Escape($_.Name) }
$pyPattern = ($pyFiles -join "|")

# Also get .bat files for CMD processes
$batFiles = Get-ChildItem -Path $scriptDir -Filter "*.bat" | ForEach-Object { [regex]::Escape($_.Name) }
$batPattern = ($batFiles -join "|")

# Also get .ps1 files for PowerShell processes (exclude this script)
$ps1Files = Get-ChildItem -Path $scriptDir -Filter "*.ps1" | Where-Object { $_.Name -ne "stop.ps1" } | ForEach-Object { [regex]::Escape($_.Name) }
$ps1Pattern = ($ps1Files -join "|")

Write-Host "Stopping all automation processes from $scriptDir..." -ForegroundColor Yellow
Write-Host ""

# Find and stop Python processes running any .py file from this directory
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -and (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine -match "($pyPattern)"
}

if ($pythonProcesses) {
    foreach ($process in $pythonProcesses) {
        $cmdLine = (Get-WmiObject Win32_Process -Filter "ProcessId = $($process.Id)" -ErrorAction SilentlyContinue).CommandLine
        Write-Host "Stopping Python process (PID: $($process.Id))..." -ForegroundColor Cyan
        Write-Host "  Command: $cmdLine" -ForegroundColor DarkGray
        Stop-Process -Id $process.Id -Force
    }
    Write-Host "Python processes stopped." -ForegroundColor Green
} else {
    Write-Host "No Python processes found." -ForegroundColor Gray
}

Write-Host ""

# Find and stop PowerShell processes running any .ps1 file from this directory
if ($ps1Pattern) {
    $psProcesses = Get-WmiObject Win32_Process -Filter "Name = 'powershell.exe'" -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -match "($ps1Pattern)"
    }

    if ($psProcesses) {
        foreach ($process in $psProcesses) {
            Write-Host "Stopping PowerShell process (PID: $($process.ProcessId))..." -ForegroundColor Cyan
            Write-Host "  Command: $($process.CommandLine)" -ForegroundColor DarkGray
            Stop-Process -Id $process.ProcessId -Force
        }
        Write-Host "PowerShell processes stopped." -ForegroundColor Green
    } else {
        Write-Host "No PowerShell processes found." -ForegroundColor Gray
    }
}

Write-Host ""

# Find and stop CMD processes running any .bat file from this directory
if ($batPattern) {
    $cmdProcesses = Get-WmiObject Win32_Process -Filter "Name = 'cmd.exe'" -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -match "($batPattern)"
    }

    if ($cmdProcesses) {
        foreach ($process in $cmdProcesses) {
            Write-Host "Stopping CMD process (PID: $($process.ProcessId))..." -ForegroundColor Cyan
            Write-Host "  Command: $($process.CommandLine)" -ForegroundColor DarkGray
            Stop-Process -Id $process.ProcessId -Force
        }
        Write-Host "CMD processes stopped." -ForegroundColor Green
    } else {
        Write-Host "No CMD processes found." -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "All automation processes have been terminated." -ForegroundColor Green
