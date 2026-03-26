"""
Capture a screenshot and save it as a JPEG in the current user's Downloads folder (Windows 11).
Requires: Pillow (see requirements-win.txt)

By default, click and drag on a dimmed fullscreen overlay to choose a rectangle, then release.

Usage:
  python screenshot.py
  screenshot.bat                     # detached so cmd does not stay open
  screenshot.vbs                     # no cmd window at all (double-click)
  screenshot.bat --full              # entire primary monitor (no selection)
  screenshot.bat --all-screens        # all monitors in one image (Windows)
"""
import argparse
import os
import sys
from datetime import datetime

from PIL import ImageGrab


def downloads_path() -> str:
    return os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Downloads")


def _ensure_win32_dpi_aware():
    """Match Tk / mouse coordinates to Pillow ImageGrab (physical pixels). Call before any GUI."""
    if sys.platform != "win32":
        return
    import ctypes

    try:
        # PROCESS_PER_MONITOR_DPI_AWARE — same idea as login.py / logout.py
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except (OSError, AttributeError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (OSError, AttributeError):
            pass


def select_region():
    """
    Fullscreen overlay: drag a rectangle. Esc cancels.
    Returns (left, top, right, bottom) for PIL crop — right/bottom exclusive — or None if cancelled.
    """
    _ensure_win32_dpi_aware()

    import tkinter as tk

    out = {"bbox": None}
    root = tk.Tk()
    root.title("")
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.35)
    root.attributes("-topmost", True)
    root.configure(bg="#1a1a1a", cursor="crosshair")

    canvas = tk.Canvas(root, highlightthickness=0, bg="#252525", cursor="crosshair")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Canvas coords for drawing; x_root/y_root for capture bbox (screen pixels, DPI-aware)
    state = {"cx0": None, "cy0": None, "sx0": None, "sy0": None, "rect": None}

    def on_press(e):
        state["cx0"] = e.x
        state["cy0"] = e.y
        state["sx0"] = e.x_root
        state["sy0"] = e.y_root
        if state["rect"] is not None:
            canvas.delete(state["rect"])
            state["rect"] = None

    def on_drag(e):
        if state["cx0"] is None:
            return
        if state["rect"] is not None:
            canvas.delete(state["rect"])
        state["rect"] = canvas.create_rectangle(
            state["cx0"],
            state["cy0"],
            e.x,
            e.y,
            outline="#ff4444",
            width=2,
        )

    def on_release(e):
        if state["sx0"] is None:
            return
        # Screen coordinates (virtual desktop origin); matches ImageGrab after DPI awareness
        x0, y0 = state["sx0"], state["sy0"]
        x1, y1 = e.x_root, e.y_root
        lx = min(x0, x1)
        uy = min(y0, y1)
        rx = max(x0, x1)
        by = max(y0, y1)
        # PIL crop: right and lower edges are exclusive
        rx += 1
        by += 1
        if rx - lx < 4 or by - uy < 4:
            out["bbox"] = None
        else:
            out["bbox"] = (lx, uy, rx, by)
        root.quit()

    def on_escape(_event=None):
        out["bbox"] = None
        root.quit()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.bind("<Escape>", on_escape)
    root.protocol("WM_DELETE_WINDOW", on_escape)
    root.focus_force()
    root.mainloop()
    try:
        root.destroy()
    except tk.TclError:
        pass
    return out["bbox"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Save a screenshot as JPEG to Downloads")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Capture the whole primary screen (skip region selection)",
    )
    parser.add_argument(
        "--all-screens",
        action="store_true",
        help="Capture all monitors in one image (Windows; Pillow; skip region selection)",
    )
    args = parser.parse_args()

    # So full-screen grabs also align with physical pixels on scaled displays
    if sys.platform == "win32" and (args.full or args.all_screens):
        _ensure_win32_dpi_aware()

    out_dir = downloads_path()
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = os.path.join(out_dir, f"screenshot_{stamp}.jpg")

    if args.all_screens and sys.platform == "win32":
        img = ImageGrab.grab(all_screens=True)
    elif args.full:
        img = ImageGrab.grab()
    else:
        try:
            bbox = select_region()
        except Exception as e:
            print(f"Region selection failed: {e}", file=sys.stderr)
            return 1
        if bbox is None:
            print("Cancelled.", file=sys.stderr)
            return 1
        img = ImageGrab.grab(bbox=bbox)

    # High quality + 4:4:4 chroma (subsampling=0) keeps text/UI edges sharper than default 4:2:0
    img.save(out_file, "JPEG", quality=96, subsampling=0, optimize=True)
    print(out_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
