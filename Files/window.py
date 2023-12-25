"""Create a window class to store window variables."""
from dataclasses import dataclass


@dataclass
class Window:
    """A window class."""

    def __init__(self, x, y, width, height):
        """Define window variables."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
