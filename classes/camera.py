"""This module contains the Camera class."""
from math import inf as infinite
from typing import Any
from game_constants.consts import GRAPHICAL_TILE_SIZE


class Camera:
    """NamedTuple-like class that represents a camera."""

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self._camera_x = x
        self._camera_y = y
        self.max_x = infinite
        self.max_y = infinite
        self.min_x = -infinite
        self.min_y = -infinite

    def __getitem__(self, obj: Any) -> int | None:
        if isinstance(obj, int):
            if obj == 0:
                return self._camera_x
            if obj == 1:
                return self._camera_y

    @property
    def x(self) -> int:
        """Returns the x coordinate of the camera.

        Returns:
            int: the x coordinate of the camera
        """
        return self._camera_x

    @property
    def y(self) -> int:
        """Returns the y coordinate of the camera.

        Returns:
            int: the y coordinate of the camera
        """
        return self._camera_y

    def move(self, dx: int, dy: int) -> None:
        """Moves the camera by dx and dy."""
        self._camera_x += dx
        if self._camera_x > self.max_x:
            self._camera_x = self.max_x
        if self._camera_x < self.min_x:
            self._camera_x = self.min_x
        self._camera_y += dy
        if self._camera_y > self.max_y:
            self._camera_y = self.max_y
        if self._camera_y < self.min_y:
            self._camera_y = self.min_y

    def set_bounds(self, screen_width: int, screen_height: int):
        """Sets the bounds of the camera.

        Sets the minimum at (0, 0) and the maximum based on the screen size
        and the desired width and height.
        """

        self.min_x = 0
        self.min_y = 0
        self.max_x = 100 * GRAPHICAL_TILE_SIZE - screen_width + 50
        self.max_y = 100 * GRAPHICAL_TILE_SIZE - screen_height
