import subprocess
import win32gui
import os
import time
import tempfile

script_dir = os.path.dirname(os.path.abspath(__file__))

# Check scheduler process (WMI works across sessions)
result = subprocess.run(
    ["powershell", "-nologo", "-noprofile", "-command",
     "Get-WmiObject Win32_Process -Filter \"commandline like '%scheduler.bat%'\" | Select-Object ProcessId"],
    capture_output=True, text=True
)
lines = [l.strip() for l in result.stdout.splitlines() if l.strip().isdigit()]
if lines:
    print(f"Scheduler: RUNNING (PID {lines[0]})")
else:
    print("Scheduler: NOT RUNNING")

# Check dialogs by running detection in session 1 via scheduled task
result_file = os.path.join(tempfile.gettempdir(), "dialog_check_result.txt")

# Remove old result file
if os.path.exists(result_file):
    os.remove(result_file)

# Inline detection script that writes result to temp file
detect_script = f"""
import win32gui
dialogs = []
def is_dialog(t):
    return 'is running' in t.lower()
def ec(h, _):
    t = win32gui.GetWindowText(h)
    if is_dialog(t): dialogs.append(t)
def et(h, _):
    t = win32gui.GetWindowText(h)
    if is_dialog(t): dialogs.append(t)
    try: win32gui.EnumChildWindows(h, ec, None)
    except: pass
win32gui.EnumWindows(et, None)
with open(r'{result_file}', 'w') as f:
    f.write('\\n'.join(dialogs) if dialogs else '0')
"""

detect_script_path = os.path.join(tempfile.gettempdir(), "dialog_detect.py")
with open(detect_script_path, "w") as f:
    f.write(detect_script)

python_exe = os.path.join(script_dir, ".venv", "Scripts", "python.exe")

# Register and run a one-shot task in session 1
ps = f'''
$action = New-ScheduledTaskAction -Execute "{python_exe}" -Argument "{detect_script_path}" -WorkingDirectory "{script_dir}"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Seconds 10)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "DialogCheck" -Action $action -Settings $settings -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName "DialogCheck"
'''
subprocess.run(["powershell", "-nologo", "-noprofile", "-command", ps], capture_output=True, text=True)

# Wait for result file (up to 8 seconds)
for _ in range(16):
    time.sleep(0.5)
    if os.path.exists(result_file):
        break

if os.path.exists(result_file):
    with open(result_file) as f:
        content = f.read().strip()
    dialogs = [d for d in content.splitlines() if d and d != "0"]
    if dialogs:
        for d in dialogs:
            print(f"Dialogs: '{d}' found!")
    else:
        print("Dialogs: none")
else:
    print("Dialogs: check timed out")
