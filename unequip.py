import pyautogui
import time
import json

# Disable fail-safe (triggered when mouse moves to screen corner)
pyautogui.FAILSAFE = False

# Load clicks from JSON file
with open("unequip.json", "r") as f:
    data = json.load(f)

clicks = data["clicks"]

print(f"Loaded {len(clicks)} clicks from unequip.json")
print("=" * 40)

# Execute each click
for i, click in enumerate(clicks, 1):
    x = click["x"]
    y = click["y"]
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

