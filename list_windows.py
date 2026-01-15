"""Helper script to list all visible windows with their titles and positions."""
import ctypes
# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import win32gui

print("=" * 70)
print("Available Windows")
print("=" * 70)

def enum_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title.strip():
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            print(f"'{title}'")
            print(f"    Handle: {hwnd}")
            print(f"    Position: ({rect[0]}, {rect[1]})")
            print(f"    Size: {width}x{height}")
            print()
    return True

win32gui.EnumWindows(enum_callback, [])

print("=" * 70)
print("Copy the window title (or part of it) to your JSON file's 'window.title' field")
