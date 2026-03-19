import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
scheduler_path = os.path.join(script_dir, "scheduler.bat")

# Register scheduler.bat as a scheduled task that runs in the user's interactive session
result = subprocess.run(
    ["schtasks", "/create", "/tn", "ClickerScheduler",
     "/tr", scheduler_path,
     "/sc", "onlogon",
     "/rl", "highest",
     "/f"],
    capture_output=True, text=True
)
print(result.stdout.strip())
if result.returncode == 0:
    print("Setup complete. Scheduler will auto-start on logon.")
    print("Use scheduler_restart.py to start/restart it now.")
else:
    print(result.stderr.strip())
