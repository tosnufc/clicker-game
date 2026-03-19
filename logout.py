import ctypes
# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
# This must be called BEFORE importing pyautogui
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import os
import pyautogui
import time
import json
import subprocess
import pygetwindow as gw
from screen_utils import get_scale_factor, scale_coords

# Disable fail-safe (triggered when mouse moves to screen corner)
pyautogui.FAILSAFE = False

# Scale coordinates from reference Full HD (1920x1080) to current screen resolution
scale = get_scale_factor()

# Find the LastZ window and bring it to the foreground
print("Looking for LastZ window...")
windows = gw.getWindowsWithTitle("LastZ")
if not windows:
    print("LastZ is not running. Nothing to close.")
    exit(0)

win = windows[0]
win.activate()
time.sleep(1)

print("LastZ window found and focused.")

# Load clicks from JSON file
with open("logout.json", "r") as f:
    data = json.load(f)

clicks = data["clicks"]

print(f"Loaded {len(clicks)} clicks from logout.json")
print("=" * 40)

# Execute each click
for i, click in enumerate(clicks, 1):
    x, y = scale_coords(click["x"], click["y"], scale)
    delay = click["delay"]
    
    # Wait before click (skip delay for first click)
    if delay > 0:
        print(f"Waiting {delay}s...")
        time.sleep(delay)
    
    # Perform click
    print(f"Click {i}: ({x}, {y})")
    pyautogui.click(x, y)

print("=" * 40)

# Gracefully close the game by sending Alt+F4
print("Closing LastZ gracefully (Alt+F4)...")
windows = gw.getWindowsWithTitle("LastZ")
if windows:
    windows[0].activate()
    time.sleep(0.5)
pyautogui.hotkey("alt", "F4")
time.sleep(5)

# Verify the game has closed; if still running, force terminate
windows = gw.getWindowsWithTitle("LastZ")
if not windows:
    print("LastZ closed successfully.")
else:
    print("LastZ is still running - force terminating process...")
    hwnd = int(windows[0]._hWnd)
    pid = ctypes.c_ulong(0)
    ctypes.windll.user32.GetWindowThreadProcessId(ctypes.c_void_p(hwnd), ctypes.byref(pid))
    process_id = pid.value
    print(f"Terminating PID {process_id}...")

    # Method 1: Use Windows API TerminateProcess directly
    PROCESS_TERMINATE = 0x0001
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(PROCESS_TERMINATE, False, process_id)
    if handle:
        if kernel32.TerminateProcess(handle, 0):
            kernel32.CloseHandle(handle)
            time.sleep(1)
        else:
            kernel32.CloseHandle(handle)
            # Method 2: Fallback to taskkill with /T (kill process tree)
            taskkill = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "taskkill.exe")
            subprocess.run([taskkill, "/PID", str(process_id), "/F", "/T"], check=False, capture_output=True)
            time.sleep(1)
    else:
        # OpenProcess failed (e.g. permission denied) - try taskkill
        taskkill = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "taskkill.exe")
        subprocess.run([taskkill, "/PID", str(process_id), "/F", "/T"], check=False, capture_output=True)
        time.sleep(1)

    windows = gw.getWindowsWithTitle("LastZ")
    if not windows:
        print("LastZ process terminated.")
    else:
        print("Warning: LastZ may still be running.")

print("Logout sequence completed!")
