"""This module contains the Tile class."""

import pygame
from .object_bases import ObjectBase

# pylint: disable=c-extension-no-member


class Tile(ObjectBase):
    """Basic reprensetation of a tile in the game. Not to be confused with the Cell class that contains multiple stacked tiles."""

    def __init__(self, 
                 walkable: bool, 
                #  image: pygame.Surface = None
                 ):
        # super().__init__(image)
        self.walkable = walkable
