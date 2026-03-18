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

# Start scheduler.bat in a new console that survives SSH disconnect
CREATE_NEW_CONSOLE = 0x00000010
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
subprocess.Popen(
    ["cmd", "/c", scheduler_path],
    cwd=script_dir,
    creationflags=CREATE_NEW_CONSOLE | CREATE_BREAKAWAY_FROM_JOB,
)
print("Started scheduler.bat in a new console window.")
