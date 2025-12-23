# PowerShell script to launch clicker.py

param([switch]$Hidden)

# If not running hidden, relaunch the script hidden
if (-not $Hidden) {
    Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$PSCommandPath`" -Hidden" -WindowStyle Hidden
    exit
}

# Change to the script directory
Set-Location "D:\dev\clicker"

# Activate the virtual environment
& "D:\dev\clicker\.venv\Scripts\Activate.ps1"

# Run the Python script
python clicker.py

