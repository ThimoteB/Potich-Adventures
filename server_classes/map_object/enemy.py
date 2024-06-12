""" This module contains the Enemy class."""
import pygame
from game_constants.consts import GRAPHICAL_TILE_SIZE

from .entity import Entity


class Enemy(Entity):
    """This class is used to create the enemy.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(
        self,
        # image: pygame.Surface,
        name: str,
        health: int,
        attack: int,
        element="Neutral",
        ia=False,
    ):
        super().__init__(name, health, attack, element)

        # self.resize(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)

        self.ia = ia
