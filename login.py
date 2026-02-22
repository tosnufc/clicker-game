import ctypes
# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
# This must be called BEFORE importing pyautogui
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import pyautogui
import time
import json
import os
from screen_utils import get_scale_factor, scale_coords

# Disable fail-safe (triggered when mouse moves to screen corner)
pyautogui.FAILSAFE = False

# Scale coordinates from reference Full HD (1920x1080) to current screen resolution
scale = get_scale_factor()

LASTZ_PATH = os.path.join(os.environ["LOCALAPPDATA"], "Last Z", "Last Z.exe")

# Launch LastZ (using os.startfile to mimic a normal double-click launch)
print("Launching LastZ...")
os.startfile(LASTZ_PATH)

# Wait for the game window to appear
print("Waiting for LastZ to load...")
time.sleep(15)

# Maximize the window
import pygetwindow as gw

for attempt in range(5):
    windows = gw.getWindowsWithTitle("LastZ")
    if windows:
        win = windows[0]
        win.maximize()
        print("LastZ window maximized.")
        break
    print(f"Window not found yet, retrying ({attempt + 1}/5)...")
    time.sleep(3)
else:
    print("Warning: Could not find LastZ window to maximize.")

# Wait a bit more for the game to settle
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
    
    # Wait before click (skip delay for first click)
    if delay > 0:
        print(f"Waiting {delay}s...")
        time.sleep(delay)
    
    # Perform click
    print(f"Click {i}: ({x}, {y})")
    pyautogui.click(x, y)

print("=" * 40)
print("Click sequence completed!")
