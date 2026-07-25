import ctypes
# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
# This must be called BEFORE importing pyautogui
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import pyautogui
import time
import random

# Ensure you have pyautogui installed: pip install pyautogui

# Give the user some time to switch to the desired window
# print("You have 1 seconds to switch to the window where you want to click...")
# time.sleep(1)

# Define the number of clicks and the interval between clicks
num_clicks = 200000000000
click_interval = 0  # seconds between clicks

# Get the current mouse position
click_x, click_y = pyautogui.position()

print(f"Click position: ({click_x}, {click_y})")

# Perform the clicks
for i in range(num_clicks):
    # Random offset within 50x50 pixel area
    offset_x = random.randint(-30, 27)
    offset_y = random.randint(-25, 26)
    click_pos_x = click_x + offset_x
    click_pos_y = click_y + offset_y

    # Perform the click
    pyautogui.click(click_pos_x, click_pos_y)
    print(f"Click {i+1} performed at position ({click_pos_x}, {click_pos_y})")
    print(f"Waiting {click_interval} second(s) until next click...")
    time.sleep(click_interval)

print("Clicking sequence completed!")