import subprocess
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
scheduler_path = os.path.join(script_dir, "scheduler.bat")
task_name = "ClickerScheduler"

# Kill any existing scheduler.bat processes by exact window title
result = subprocess.run(
    ["taskkill", "/f", "/fi", "WINDOWTITLE eq Administrator:  Scheduler - 24/7 Workflow Launcher"],
    capture_output=True, text=True
)
if "SUCCESS" not in result.stdout:
    result = subprocess.run(
        ["taskkill", "/f", "/fi", "WINDOWTITLE eq Scheduler - 24/7 Workflow Launcher"],
        capture_output=True, text=True
    )
print(result.stdout.strip())
print(result.stderr.strip())

if "SUCCESS" in result.stdout:
    print("Killed existing scheduler process. Waiting 3 seconds...")
    time.sleep(3)
else:
    print("No existing scheduler process found.")

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
    ["powershell", "-nologo", "-noprofile", "-command", ps_script],
    capture_output=True, text=True
)

if "OK" in result.stdout:
    print("Started scheduler in desktop session.")
else:
    print("Failed to start scheduler:")
    print(result.stdout.strip())
    print(result.stderr.strip())
