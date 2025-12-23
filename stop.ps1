# PowerShell script to force stop clicker.py processes

Write-Host "Stopping clicker processes..." -ForegroundColor Yellow

# Find and stop Python processes running clicker.py
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -and (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*clicker.py*"
}

if ($pythonProcesses) {
    foreach ($process in $pythonProcesses) {
        Write-Host "Stopping Python process (PID: $($process.Id))..." -ForegroundColor Cyan
        Stop-Process -Id $process.Id -Force
    }
    Write-Host "Python processes stopped." -ForegroundColor Green
} else {
    Write-Host "No Python clicker processes found." -ForegroundColor Gray
}

# Find and stop PowerShell processes running clicker.ps1
$psProcesses = Get-WmiObject Win32_Process -Filter "Name = 'powershell.exe'" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*clicker.ps1*"
}

if ($psProcesses) {
    foreach ($process in $psProcesses) {
        Write-Host "Stopping PowerShell process (PID: $($process.ProcessId))..." -ForegroundColor Cyan
        Stop-Process -Id $process.ProcessId -Force
    }
    Write-Host "PowerShell processes stopped." -ForegroundColor Green
} else {
    Write-Host "No PowerShell clicker processes found." -ForegroundColor Gray
}

Write-Host "`nAll clicker processes have been terminated." -ForegroundColor Green

