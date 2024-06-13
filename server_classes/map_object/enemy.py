""" This module contains the Enemy class."""

from .entity import Entity
from server_classes.goal.goal import Goal
from server_classes.goal.playerGoal import playerGoal
from server_classes.goal.cardGoal import cardGoal
import random


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
        self._goal:Goal|None=None

        # self.resize(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)

        self.ia = ia
        
    @property
    def goal(self)->Goal:
        return self._goal
    
    @goal.setter
    def goal(self, goal:Goal)->None:
        self._goal=goal


if __name__ == "__main__":
    try:
        enemy = Enemy("test", 10, 10)
        # get the current ememy's goal
        enemy.goal = playerGoal()
        goal = enemy.goal
        if goal is None:
            enemy.goal = playerGoal()
        elif random.random() <= goal.change_probability:
            card=cardGoal()
            player=playerGoal()
            weight=card.weight+player.weight
            
            hasard=random.random()
            if hasard*weight<=card.weight:
                enemy.goal=card
            else:
                enemy.goal=player
        
        enemy.goal.regression()
        print(enemy.goal)
    except Exception as e:
        print(e)