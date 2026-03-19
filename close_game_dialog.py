import subprocess
import os
import sys
import time
import tempfile

script_dir = os.path.dirname(os.path.abspath(__file__))
python_exe = os.path.join(script_dir, ".venv", "Scripts", "python.exe")
result_file = os.path.join(tempfile.gettempdir(), "close_dialog_result.txt")

# Remove old result file
if os.path.exists(result_file):
    os.remove(result_file)

# Inline script that runs in session 1 to find and close dialogs
close_script = f"""
import win32gui
import win32con

found = []

def enum_child(hwnd, parent_hwnd):
    title = win32gui.GetWindowText(hwnd)
    cls = win32gui.GetClassName(hwnd)
    if 'is running' in title.lower():
        found.append(('dialog', parent_hwnd, title))
    if cls == 'Button' and title.strip().upper() == 'OK':
        found.append(('button', hwnd, title))

def enum_top(hwnd, _):
    title = win32gui.GetWindowText(hwnd)
    if 'is running' in title.lower():
        found.append(('dialog', hwnd, title))
    try:
        win32gui.EnumChildWindows(hwnd, enum_child, hwnd)
    except:
        pass

win32gui.EnumWindows(enum_top, None)

closed = set()
for kind, hwnd, title in found:
    if hwnd in closed:
        continue
    if kind == 'button':
        win32gui.PostMessage(hwnd, win32con.BM_CLICK, 0, 0)
    else:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    closed.add(hwnd)

with open(r'{result_file}', 'w') as f:
    f.write(str(len(closed)))
"""

close_script_path = os.path.join(tempfile.gettempdir(), "close_dialog_task.py")
with open(close_script_path, "w") as f:
    f.write(close_script)

# Run in session 1 via scheduled task
ps = f'''
$action = New-ScheduledTaskAction -Execute "{python_exe}" -Argument "{close_script_path}" -WorkingDirectory "{script_dir}"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Seconds 10)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName "CloseDialogs" -Action $action -Settings $settings -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName "CloseDialogs"
'''
subprocess.run(["powershell", "-nologo", "-noprofile", "-command", ps], capture_output=True, text=True)

# Wait for result (up to 8 seconds)
for _ in range(16):
    time.sleep(0.5)
    if os.path.exists(result_file):
        break

if os.path.exists(result_file):
    with open(result_file) as f:
        count = int(f.read().strip() or "0")
    if count > 0:
        print(f"Dismissed {count} dialog(s).")
    else:
        print("No dialogs found.")
else:
    print("Dialog close timed out.")

print("Running logout.py...")
subprocess.run([sys.executable, os.path.join(script_dir, "logout.py")])
