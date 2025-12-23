import pyautogui
import time

# Ensure you have pyautogui installed: pip install pyautogui

# Give the user some time to switch to the desired window
# print("You have 1 seconds to switch to the window where you want to click...")
# time.sleep(1)

# Define the number of clicks and the interval between clicks
num_clicks = 20000
click_interval = 0.005  # seconds between clicks

# Get the current mouse position
click_x, click_y = pyautogui.position()

print(f"Click position: ({click_x}, {click_y})")

# Perform the clicks
for i in range(num_clicks):
    # Perform the click
    pyautogui.click(click_x, click_y)
    print(f"Click {i+1} performed at position ({click_x}, {click_y})")
    print(f"Waiting {click_interval} second(s) until next click...")
    time.sleep(click_interval)

print("Clicking sequence completed!")