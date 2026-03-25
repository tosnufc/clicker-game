import subprocess
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
scheduler_path = os.path.join(script_dir, "scheduler.bat")
task_name = "ClickerScheduler"

# Kill scheduler-related processes: cmd running scheduler.bat AND python running scheduler_runner.py.
# The old logic only matched cmd.exe + scheduler.bat, so python.exe kept running and a second
# scheduler stacked on top.
KILL_PS = r"""
$tk = Join-Path $env:SystemRoot 'System32\taskkill.exe'
$procs = @()
try {
    $procs = Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object {
        $c = $_.CommandLine
        if (-not $c) { return $false }
        return ($c -like '*scheduler.bat*' -or $c -like '*scheduler_runner.py*')
    }
} catch {
    $procs = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object {
        $c = $_.CommandLine
        if (-not $c) { return $false }
        return ($c -like '*scheduler.bat*' -or $c -like '*scheduler_runner.py*')
    }
}
if ($null -eq $procs) { $procs = @() }
$procs = @($procs)
$seen = @{}
foreach ($p in $procs) {
    $id = [int]$p.ProcessId
    if ($seen.ContainsKey($id)) { continue }
    $seen[$id] = $true
    & $tk /F /T /PID $id 2>$null | Out-Null
}
if ($seen.Count -gt 0) { $seen.Keys -join ',' } else { '' }
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", KILL_PS],
    capture_output=True,
    text=True,
)
killed = [x.strip() for x in (result.stdout or "").split(",") if x.strip().isdigit()]
if killed:
    print(f"Killed scheduler-related process tree(s): PID {', '.join(killed)}")
    print("Waiting 3 seconds...")
    time.sleep(3)
else:
    print("No existing scheduler process found (scheduler.bat / scheduler_runner.py).")

# Register and start the scheduled task via PowerShell for full control
ps_script = f'''
$action = New-ScheduledTaskAction -Execute "{scheduler_path}" -WorkingDirectory "{script_dir}"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit ([TimeSpan]::Zero)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "{task_name}" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName "{task_name}"
Write-Output "OK"
'''

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_script],
    capture_output=True,
    text=True,
)

if "OK" in result.stdout:
    print("Started scheduler in desktop session.")
else:
    print("Failed to start scheduler:")
    print(result.stdout.strip())
    print(result.stderr.strip())
