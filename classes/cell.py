""" This file contains the case class that will represent the cases on the board. """

from __future__ import annotations
import pygame
from game_constants.consts import GRAPHICAL_TILE_SIZE
from .camera import Camera
from .map_object import Tile, AnimatedTile, Pawn, Enemy


class Cell:  # pylint: disable=too-many-instance-attributes
    """This class represents a higler level abstraction of a tilemap cell.

    It contains all the tiles that are present in the cell
    handles the resizing of those tiles and the drawing of the cell.
    It can contain a game object, which can be used to represent a player, an enemy, an item, etc.
    """

    cell_mapping: dict[tuple[int, int], Cell] = {}

    def __init__(
        self, x: int, y: int, width: int, height: int, rect: bool = False
    ) -> None:
        """Initializes the cell.

        Args:
            x (int): X coordinate of the cell.
            y (int): Y coordinate of the cell.
            width (int): Width of the cell.
            height (int): Height of the cell.
            rect (bool, optional): Whether the cell is a rectangle or not. Defaults to False.
        """
        self.cell_mapping[(x, y)] = self

        self.x = x
        self.y = y
        self.rect = rect
        self.highlighted = False
        self.layers: list[Tile | AnimatedTile] = []
        self.width = width
        self.height = height
        self.game_object = None
        self.highlight_color = (0, 255, 0)
        self._heal_value = 0
        self.is_heal_cell = False

    @property
    def heal_value(self) -> int:
        return self._heal_value

    @heal_value.setter
    def heal_value(self, value: int) -> None:
        self._heal_value = value
        self.is_heal_cell = True

    def add_layer(self, layer: Tile) -> None:
        """Adds a layer to the cell.

        Args:
            layer (Tile): The layer to add.
        """
        self.layers.append(layer)

    def resize(self, width: int, height: int) -> None:
        """Resizes the cell.

        Args:
            width (int): Width of the cell.
            height (int): Height of the cell.
        """
        for tile in self.layers:
            tile.resize(width, height)

    def draw(self, surface: pygame.surface.Surface, camera: Camera) -> None:
        """Draws the cell on the screen.

        Args:
            surface (pygame.surface.Surface): The surface to draw the cell on.
            camera (Camera): The camera instance.
        """
        for tile in self.layers:
            tile.draw(
                self.x * GRAPHICAL_TILE_SIZE,
                self.y * GRAPHICAL_TILE_SIZE,
                surface,
                camera,
            )
        if self.game_object:
            self.game_object.draw(
                self.x * GRAPHICAL_TILE_SIZE,
                self.y * GRAPHICAL_TILE_SIZE,
                surface,
                camera,
            )

        if self.highlighted:
            # Draw a green rectangle around the cell
            highlight_rect = pygame.Rect(
                self.x * GRAPHICAL_TILE_SIZE - camera.x,
                self.y * GRAPHICAL_TILE_SIZE - camera.y,
                GRAPHICAL_TILE_SIZE,
                GRAPHICAL_TILE_SIZE,
            )
            pygame.draw.rect(surface, self.highlight_color, highlight_rect, 2, 10)

    def tick(self, frame_id: int) -> None:
        """Ticks the cell.

        Args:
            frame_id (int): The current frame id.
        """
        for tile in self.layers:
            tile.tick(frame_id)
        if self.game_object:
            self.game_object.tick(frame_id)

    def remove_object(self) -> None:
        """Removes the object from the cell."""
        self.game_object = None

    def add_pawn(self, pawn: Pawn) -> None:
        """Adds a pawn to the cell.

        Args:
            pawn (Pawn): The pawn to add.
        """
        self.game_object = pawn

    def add_enemy(self, enemy: Enemy) -> None:
        """Adds an enemy to the cell.

        Args:
            enemy (Pawn): The enemy to add.
        """
        self.game_object = enemy

    def get_coordinates(self) -> tuple[int, int]:
        """Returns the coordinates of the cell.

        Returns:
            tuple[int, int]: The coordinates of the cell.
        """
        return self.x, self.y

    # TODO - Transformer ces méthodes en property
    def has_pawn(self):
        """Returns whether the cell has a pawn or not.

        Returns:
            bool: Whether the cell has a pawn or not.
        """
        return isinstance(self.game_object, Pawn)

    def has_enemy(self):
        """Returns whether the cell has an enemy or not.

        Returns:
            bool: Whether the cell has an enemy or not.
        """
        return isinstance(self.game_object, Enemy)

    @property
    def is_empty(self) -> bool:
        """Returns whether the cell is empty or not.

        Returns:
            bool: Whether the cell is empty or not.
        """
        return self.game_object is None

    def highlight(
        self,
        color: tuple[int, int, int] = (0, 255, 0),
    ) -> None:
        """Highlights the cell."""
        self.highlight_color = color
        self.highlighted = True

    def unhighlight(self) -> None:
        """Unhighlights the cell."""
        self.highlighted = False

    @property
    def walkable(self) -> bool:
        """Returns whether the cell is walkable or not.

        Returns:
            bool: Whether the cell is walkable or not.
        """
        return all(tile.walkable for tile in self.layers)
