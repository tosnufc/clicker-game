"""
Utility for scaling mouse click coordinates across different screen resolutions.

JSON files contain click coordinates recorded at Full HD (1920x1080).
This module scales them to the current screen resolution, supporting any
16:9 display (e.g., Full HD 1920x1080, 4K 3840x2160).
"""

import pyautogui

# Reference resolution - coordinates in JSON files were recorded at this resolution
REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080


def get_scale_factor():
    """Get scale factor from reference resolution (1920x1080) to current screen."""
    screen_width, _ = pyautogui.size()
    return screen_width / REFERENCE_WIDTH


def scale_coords(x, y, scale):
    """Scale x, y coordinates by the given scale factor."""
    return round(x * scale), round(y * scale)
