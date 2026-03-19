import win32gui
import win32con
import subprocess
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))

def find_and_close_dialogs():
    found = []

    def enum_child(hwnd, parent_hwnd):
        title = win32gui.GetWindowText(hwnd)
        cls = win32gui.GetClassName(hwnd)
        # Match "Game Is Running" label or its parent dialog (#32770)
        if "game is running" in title.lower():
            found.append(('dialog', parent_hwnd, title))
        # Match OK buttons inside dialogs
        if cls == "Button" and title.strip().upper() == "OK":
            found.append(('button', hwnd, title))

    def enum_top(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if "game is running" in title.lower():
            found.append(('dialog', hwnd, title))
        try:
            win32gui.EnumChildWindows(hwnd, enum_child, hwnd)
        except Exception:
            pass

    win32gui.EnumWindows(enum_top, None)

    if not found:
        print("No 'Game Is Running' dialog found.")
        return False

    closed = set()
    for kind, hwnd, title in found:
        if hwnd in closed:
            continue
        if kind == 'button':
            print(f"Clicking OK button (hwnd={hwnd})")
            win32gui.PostMessage(hwnd, win32con.BM_CLICK, 0, 0)
        else:
            print(f"Closing dialog: '{title}' (hwnd={hwnd})")
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        closed.add(hwnd)

    print(f"Dismissed {len(closed)} dialog(s).")
    return True

find_and_close_dialogs()

print("Running logout.py...")
subprocess.run(
    [sys.executable, os.path.join(script_dir, "logout.py")],
)
