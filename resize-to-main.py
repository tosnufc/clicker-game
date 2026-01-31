"""Resizes Farmer and No-buy windows to match the size of Main window."""
import ctypes
# Make Python DPI-aware to get correct screen coordinates on Windows 10/11
ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE

import win32gui
import win32con

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

def resize_to_main():
    """Resize Farmer and No-buy to match Main's size."""
    print("Resizing windows to match Main...")
    print("-" * 40)
    
    # Find Main window and get its size
    main_hwnd = find_window_by_exact_title("Main")
    if not main_hwnd:
        print("  Error: 'Main' window not found!")
        return
    
    main_rect = win32gui.GetWindowRect(main_hwnd)
    main_width = main_rect[2] - main_rect[0]
    main_height = main_rect[3] - main_rect[1]
    print(f"  Main size: {main_width}x{main_height}")
    
    # Resize other windows
    windows_to_resize = ["Farmer", "No-buy"]
    resized = 0
    
    for name in windows_to_resize:
        hwnd = find_window_by_exact_title(name)
        
        if hwnd:
            try:
                # Get current position
                rect = win32gui.GetWindowRect(hwnd)
                x, y = rect[0], rect[1]
                
                # Resize keeping same position
                win32gui.SetWindowPos(
                    hwnd,
                    win32con.HWND_TOP,
                    x, y, main_width, main_height,
                    win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
                )
                print(f"  Resized: '{name}' to {main_width}x{main_height}")
                resized += 1
            except Exception as e:
                print(f"  Failed: '{name}' - {e}")
        else:
            print(f"  Not found: '{name}'")
    
    print("-" * 40)
    print(f"Resized {resized}/{len(windows_to_resize)} windows")

if __name__ == "__main__":
    resize_to_main()
