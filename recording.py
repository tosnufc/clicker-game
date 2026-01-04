from pynput import mouse, keyboard
import time
import json
import threading

# Store recorded clicks
clicks = []
last_click_time = None
running = True

def on_click(x, y, button, pressed):
    global last_click_time
    
    if not running:
        return False
    
    # Only record left clicks when pressed (not released)
    if button == mouse.Button.left and pressed:
        current_time = time.time()
        
        # Calculate delay from last click
        if last_click_time is None:
            delay = 0
        else:
            delay = round(current_time - last_click_time, 3)
        
        last_click_time = current_time
        
        click_data = {"x": x, "y": y, "delay": delay}
        clicks.append(click_data)
        print(f"Recorded click #{len(clicks)}: ({x}, {y}) - delay: {delay}s")

def on_press(key):
    global running
    
    if key == keyboard.Key.esc:
        running = False
        print("\nEscape pressed. Stopping recording...")
        return False

def save_clicks():
    output = {"clicks": clicks}
    with open("clicks.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved {len(clicks)} clicks to clicks.json")

# Main
print("=" * 50)
print("Mouse Click Recorder")
print("=" * 50)
print("Left-click anywhere to record positions and timing.")
print("Press ESCAPE to stop recording and save to clicks.json")
print("=" * 50)
print()

# Start keyboard listener in a separate thread
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Start mouse listener (blocking)
with mouse.Listener(on_click=on_click) as mouse_listener:
    while running:
        time.sleep(0.1)

# Save recorded clicks
if clicks:
    save_clicks()
else:
    print("No clicks recorded.")

print("Recording finished!")

