import subprocess
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
scheduler_path = os.path.join(script_dir, "scheduler.bat")

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

# Start scheduler.bat via WMI (creates process outside SSH job object)
result = subprocess.run(
    ["powershell", "-nologo", "-noprofile", "-command",
     f'Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList \'cmd.exe /c "{scheduler_path}"\''],
    capture_output=True, text=True
)
if "ReturnValue" in result.stdout and ": 0" in result.stdout:
    print("Started scheduler.bat successfully.")
else:
    print("Failed to start scheduler.bat:")
    print(result.stdout.strip())
    print(result.stderr.strip())
