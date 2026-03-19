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

# Check if the scheduled task exists
check = subprocess.run(
    ["schtasks", "/query", "/tn", "ClickerScheduler"],
    capture_output=True, text=True
)
if check.returncode != 0:
    print("Task 'ClickerScheduler' not found. Running setup...")
    subprocess.run(
        ["schtasks", "/create", "/tn", "ClickerScheduler",
         "/tr", scheduler_path,
         "/sc", "onlogon",
         "/rl", "highest",
         "/f"],
        capture_output=True, text=True
    )

# Start scheduler via schtasks (runs in user's interactive desktop session)
result = subprocess.run(
    ["schtasks", "/run", "/tn", "ClickerScheduler"],
    capture_output=True, text=True
)
if "SUCCESS" in result.stdout:
    print("Started scheduler in desktop session.")
else:
    print("Failed to start scheduler:")
    print(result.stdout.strip())
    print(result.stderr.strip())
