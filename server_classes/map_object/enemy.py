""" This module contains the Enemy class."""

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
        self.chase_player: float = 0
        self.chase_card: float = 0
        self.previous_choice_enemy: str = ""

        # self.resize(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)

        self.ia = ia
