import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import pyautogui
import time
import json
from screen_utils import get_scale_factor, scale_coords

pyautogui.FAILSAFE = False

REPEAT_COUNT = 100000000
SEQUENCE_DELAY = 0

scale = get_scale_factor()

with open("bounty.json", "r") as f:
    data = json.load(f)

clicks = data["clicks"]

print(f"Loaded {len(clicks)} clicks from bounty.json")
print(f"Repeating {REPEAT_COUNT} times with {SEQUENCE_DELAY}s delay between sequences")
print("=" * 40)

for run in range(1, REPEAT_COUNT + 1):
    print(f"\n--- Run {run}/{REPEAT_COUNT} ---")
    for i, click in enumerate(clicks, 1):
        x, y = scale_coords(click["x"], click["y"], scale)
        delay = click["delay"]
        if delay > 0:
            print(f"Waiting {delay}s...")
            time.sleep(delay)
        print(f"Click {i}: ({x}, {y})")
        pyautogui.click(x, y)
    if run < REPEAT_COUNT:
        print(f"Waiting {SEQUENCE_DELAY}s before next run...")
        time.sleep(SEQUENCE_DELAY)

print("=" * 40)
print("All sequences completed!")
