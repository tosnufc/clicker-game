import ctypes
# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
# This must be called BEFORE importing pyautogui
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import pyautogui
import time
import json
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

# Verify the game has closed
windows = gw.getWindowsWithTitle("LastZ")
if not windows:
    print("LastZ closed successfully.")
else:
    print("LastZ is still running - it may need a confirmation click to close.")

print("Logout sequence completed!")
