"""Restores window positions from formation-2.json."""
import ctypes
# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import win32gui
import win32con
import json
import os

FORMATION_FILE = "formation-2.json"

def find_window_by_exact_title(target_title):
    """Find a window handle by exact title match."""
    result = None
    
    def enum_callback(hwnd, _):
        nonlocal result
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title == target_title:
                result = hwnd
                return False  # Stop enumeration
        return True
    
    win32gui.EnumWindows(enum_callback, None)
    return result

def restore_formation():
    """Restore window positions from JSON file."""
    # Load positions from JSON
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, FORMATION_FILE)
    
    if not os.path.exists(json_path):
        print(f"Error: {FORMATION_FILE} not found!")
        return
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    windows = data.get("windows", [])
    print(f"Restoring {len(windows)} window positions from {FORMATION_FILE}...")
    print("-" * 40)
    
    restored = 0
    for w in windows:
        name = w["title"]
        hwnd = find_window_by_exact_title(name)
        
        if hwnd:
            try:
                # Restore window if minimized
                placement = win32gui.GetWindowPlacement(hwnd)
                if placement[1] == win32con.SW_SHOWMINIMIZED:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                
                # Move and resize window
                win32gui.SetWindowPos(
                    hwnd,
                    win32con.HWND_TOP,
                    w["x"], w["y"], w["width"], w["height"],
                    win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
                )
                print(f"  Restored: '{name}'")
                restored += 1
            except Exception as e:
                print(f"  Failed: '{name}' - {e}")
        else:
            print(f"  Not found: '{name}'")
    
    print("-" * 40)
    print(f"Restored {restored}/{len(windows)} windows")

if __name__ == "__main__":
    restore_formation()
