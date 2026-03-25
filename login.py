import ctypes
from ctypes import wintypes

# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
# This must be called BEFORE importing pyautogui
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import pyautogui
import time
import json
import os
import subprocess
import pygetwindow as gw
from screen_utils import get_scale_factor, scale_coords

# Disable fail-safe (triggered when mouse moves to screen corner)
pyautogui.FAILSAFE = False

# Scale coordinates from reference Full HD (1920x1080) to current screen resolution
scale = get_scale_factor()

LASTZ_DIR = os.path.join(os.environ["LOCALAPPDATA"], "Last Z")
LASTZ_PATH = os.path.join(LASTZ_DIR, "Last Z.exe")
TASKKILL = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "taskkill.exe")

# Kill passes: repeat until none left, up to this many rounds (each round may find new PIDs)
TERMINATE_MAX_PASSES = 3
# After launch, how often to look for the game window
WINDOW_FIND_ATTEMPTS = 4

WM_CLOSE = 0x0010


def dismiss_is_running_dialogs():
    """Close windows whose title contains 'is running' (e.g. Launcher is Running)."""
    closed = []

    def enum_proc(hwnd, _):
        if not ctypes.windll.user32.IsWindowVisible(hwnd):
            return True
        n = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        if n == 0:
            return True
        buf = ctypes.create_unicode_buffer(n + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, n + 1)
        title = buf.value.strip()
        if title and "is running" in title.lower():
            ctypes.windll.user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
            closed.append(title)
        return True

    callback = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(enum_proc)
    ctypes.windll.user32.EnumWindows(callback, 0)
    if closed:
        print(f"Dismissed dialog(s): {closed}")
        time.sleep(1)


def terminate_lastz():
    """Kill every process tied to Last Z (path or command line). Repeat until none left."""
    ps = """
    Get-CimInstance Win32_Process | Where-Object {
        ($_.ExecutablePath -and $_.ExecutablePath -like '*Last Z*') -or
        ($_.CommandLine -and $_.CommandLine -like '*Last Z*')
    } | ForEach-Object { $_.ProcessId }
    """
    for pass_num in range(TERMINATE_MAX_PASSES):
        r = subprocess.run(
            ["powershell", "-nologo", "-noprofile", "-command", ps],
            capture_output=True,
            text=True,
            timeout=20,
        )
        pids = sorted(
            {ln.strip() for ln in (r.stdout or "").strip().splitlines() if ln.strip().isdigit()}
        )
        if not pids:
            break
        for pid in pids:
            subprocess.run([TASKKILL, "/PID", pid, "/F", "/T"], capture_output=True)
        print(f"Terminated {len(pids)} Last Z process(es) (cleanup pass {pass_num + 1})")
        dismiss_is_running_dialogs()
        time.sleep(2)
    dismiss_is_running_dialogs()
    time.sleep(4)


def find_lastz_window():
    """Find the game window; title may be 'LastZ', 'Last Z', etc."""
    bad_substrings = ("is running",)
    for w in gw.getAllWindows():
        if not w.visible or not w.title:
            continue
        t = w.title.strip()
        tl = t.lower()
        if any(b in tl for b in bad_substrings):
            continue
        compact = "".join(c.lower() for c in t if c.isalnum())
        if "lastz" in compact or "last z" in tl:
            return w
        if "survival" in tl and len(t) >= 4:
            return w
    return None


def focus_and_maximize_lastz():
    win = find_lastz_window()
    if win:
        try:
            win.activate()
            time.sleep(0.3)
            win.maximize()
        except Exception:
            pass
        return True
    return False


# Clean exit: kill Last Z tree, close stale dialogs, wait for mutex to clear
terminate_lastz()
dismiss_is_running_dialogs()

print("Launching LastZ...")
os.startfile(LASTZ_PATH)

print("Waiting for LastZ to load...")
time.sleep(12)

found = False
for attempt in range(WINDOW_FIND_ATTEMPTS):
    dismiss_is_running_dialogs()
    if focus_and_maximize_lastz():
        print("LastZ window found and maximized.")
        found = True
        break
    print(f"Window not found yet, retrying ({attempt + 1}/{WINDOW_FIND_ATTEMPTS})...")
    time.sleep(5)

if not found:
    print("Warning: Could not find LastZ window to maximize.")

time.sleep(3)

# Load clicks from JSON file
with open("login.json", "r") as f:
    data = json.load(f)

clicks = data["clicks"]

print(f"Loaded {len(clicks)} clicks from login.json")
print("=" * 40)

# Execute each click
for i, click in enumerate(clicks, 1):
    x, y = scale_coords(click["x"], click["y"], scale)
    delay = click["delay"]

    if delay > 0:
        print(f"Waiting {delay}s...")
        time.sleep(delay)

    print(f"Click {i}: ({x}, {y})")
    pyautogui.click(x, y)

print("=" * 40)
print("Click sequence completed!")
