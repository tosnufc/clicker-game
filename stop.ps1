# PowerShell script to force stop clicker.py, saga.py, and boomer.py processes

param([switch]$Hidden)

# If not running hidden, relaunch the script hidden
if (-not $Hidden) {
    Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$PSCommandPath`" -Hidden" -WindowStyle Hidden
    exit
}

Write-Host "Stopping clicker, saga, and boomer processes..." -ForegroundColor Yellow

# Find and stop Python processes running clicker.py or saga.py
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -and (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine -match "(clicker\.py|saga\.py|boomer\.py)"
}

if ($pythonProcesses) {
    foreach ($process in $pythonProcesses) {
        Write-Host "Stopping Python process (PID: $($process.Id))..." -ForegroundColor Cyan
        Stop-Process -Id $process.Id -Force
    }
    Write-Host "Python processes stopped." -ForegroundColor Green
} else {
    Write-Host "No Python clicker/saga/boomer processes found." -ForegroundColor Gray
}

# Find and stop PowerShell processes running clicker.ps1 or saga.ps1
$psProcesses = Get-WmiObject Win32_Process -Filter "Name = 'powershell.exe'" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "(clicker\.ps1|saga\.ps1|boomer\.ps1)"
}

if ($psProcesses) {
    foreach ($process in $psProcesses) {
        Write-Host "Stopping PowerShell process (PID: $($process.ProcessId))..." -ForegroundColor Cyan
        Stop-Process -Id $process.ProcessId -Force
    }
    Write-Host "PowerShell processes stopped." -ForegroundColor Green
} else {
    Write-Host "No PowerShell clicker/saga/boomer processes found." -ForegroundColor Gray
}

# Find and stop CMD processes running saga.bat
$cmdProcesses = Get-WmiObject Win32_Process -Filter "Name = 'cmd.exe'" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "(saga\.bat|boomer\.bat)"
}

if ($cmdProcesses) {
    foreach ($process in $cmdProcesses) {
        Write-Host "Stopping CMD process (PID: $($process.ProcessId))..." -ForegroundColor Cyan
        Stop-Process -Id $process.ProcessId -Force
    }
    Write-Host "CMD processes stopped." -ForegroundColor Green
} else {
    Write-Host "No CMD saga/boomer processes found." -ForegroundColor Gray
}

Write-Host "`nAll clicker, saga, and boomer processes have been terminated." -ForegroundColor Green
