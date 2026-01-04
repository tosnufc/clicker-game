import pyautogui
import time
import json

# Disable fail-safe (triggered when mouse moves to screen corner)
pyautogui.FAILSAFE = False

# Configuration
REPEAT_COUNT = 10
SEQUENCE_DELAY = 90  # seconds between sequences

# Load clicks from JSON file
with open("saga.json", "r") as f:
    data = json.load(f)

clicks = data["clicks"]

print(f"Loaded {len(clicks)} clicks from saga.json")
print(f"Will repeat {REPEAT_COUNT} times with {SEQUENCE_DELAY}s delay between sequences")
print("=" * 40)

# Repeat the sequence
for seq in range(1, REPEAT_COUNT + 1):
    print(f"\n>>> Sequence {seq}/{REPEAT_COUNT}")
    print("-" * 40)
    
    # Execute each click in the sequence
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
    
    # Wait between sequences (skip after last sequence)
    if seq < REPEAT_COUNT:
        print(f"\nWaiting {SEQUENCE_DELAY}s before next sequence...")
        time.sleep(SEQUENCE_DELAY)

print("\n" + "=" * 40)
print("All sequences completed!")
