import subprocess
import win32gui

# Check scheduler process
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

# Check for Game Is Running dialogs
dialogs = []

def enum_child(hwnd, _):
    title = win32gui.GetWindowText(hwnd)
    if "game is running" in title.lower():
        dialogs.append(title)

def enum_top(hwnd, _):
    title = win32gui.GetWindowText(hwnd)
    if "game is running" in title.lower():
        dialogs.append(title)
    try:
        win32gui.EnumChildWindows(hwnd, enum_child, None)
    except Exception:
        pass

win32gui.EnumWindows(enum_top, None)

if dialogs:
    print(f"Dialogs: {len(dialogs)} 'Game Is Running' dialog(s) found!")
else:
    print("Dialogs: none")
