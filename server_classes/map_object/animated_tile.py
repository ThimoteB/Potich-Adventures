# """This module contains the AnimatedTile class."""
# import pygame

# from game_constants.consts import TICK_RATE
# from .object_bases import AnimatedObjectBase


# class AnimatedTile(AnimatedObjectBase):
#     """Basic representation of an animated tile in the game.TiledMap
#     Handles automagically the animation of the tile and its timing."""

#     def __init__(
#         self,
#         walkable: bool,
#         frames: list[pygame.Surface],
#         frame_durations: list[int],
#         reverse_at_end: bool = True,
#     ):
#         super().__init__(frame_durations, reverse_at_end)
#         self.walkable = walkable
