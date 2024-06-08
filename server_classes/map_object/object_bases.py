"""Module containing the base class of all the map objects 
(objects that will eventually be drawn on the map)."""

import logging
from abc import ABC, abstractmethod

import pygame

from game_constants.consts import TICK_DURATION_MS

# pylint: disable=c-extension-no-member

log = logging.getLogger(__name__)


class ObjectBaseInterface(ABC):
    """Base interface that will be inherited by bases classes that actually implement the methods

    Note : Abstract methods don't need to be called with super().
    """

    # @abstractmethod
    # def draw(
    #     self,
    #     x: int,
    #     y: int,
    #     surface: pygame.surface.Surface,
    #     camera: tuple[int, int],
    # ) -> None:
    #     """Base draw method that will draw the object on the screen."""

    @abstractmethod
    def tick(self, frame_id: int):
        """Base tick method that will update the object's state. Could be animation or
        something changing over time."""

    # @abstractmethod
    # def resize(self, width: int, height: int) -> None:
    #     """Resize the object to be drawn smaller or larger on the screen."""


class ObjectBase(ObjectBaseInterface):
    """Base class of all the map objects."""

    def __init__(self):
        pass

    # def draw(
    #     self,
    #     x: int,
    #     y: int,
    #     surface: pygame.surface.Surface,
    #     camera: tuple[int, int],
    # ) -> None:
    #     """Draws the object on the screen."""
    #     if self._image:
    #         surface.blit(self._image, (x - camera[0], y - camera[1]))

    def tick(self, frame_id: int) -> None:
        """Ticks the object."""

    # def resize(self, width: int, height: int) -> None:
    #     """Resizes the object's image."""
    #     if self._image:
    #         self._image = pygame.transform.scale(self._image, (width, height))


# class AnimatedObjectBase(ObjectBase, ObjectBaseInterface):
#     """Base class for all the animated objects (objects with frames)."""

#     def __init__(
#         self,
#         # frames: list[pygame.Surface],
#         frame_durations: list[int],
#         reverse_at_end: bool = True,
#     ):
#         """Instanciator for the animated objects.

#         Args:
#             frames (list[pygame.Surface]): list of frames
#             frame_durations (list[int]): frame duration in ms for each frame.
#             reverse_at_end (bool, optional): Reverse the animation when the end is reached. Defaults to True.
#         """

#         super().__init__()  # Init parce que c'est "plus propre"

#         # Reverse frames if necessary
#         if reverse_at_end:
#             frames = frames + frames[-2:2:-1]
#             frame_durations = frame_durations + frame_durations[-2:2:-1]

#         self.frames = frames
#         self.current_frame = 0
#         self.frame_durations = frame_durations  # in ms

#         self.cumulative_frame_durations = [
#             sum(frame_durations[: i + 1]) for i in range(len(frame_durations))
#         ]

    def tick(self, frame_id: int) -> None:
        """Updates the object's animation.

        Args:
            global_tick_number (int): The global tick number of the game.
        """

        animation_tick_number = frame_id * TICK_DURATION_MS
        animation_tick_number = (
            animation_tick_number % self.cumulative_frame_durations[-1]
        )

        # reset animation if necessary
        if animation_tick_number > self.cumulative_frame_durations[-1]:
            self.current_frame = 0
            return

        # find current frame
        for i, frame_duration in enumerate(self.cumulative_frame_durations):
            if animation_tick_number < frame_duration:
                self.current_frame = i
                break

    # def resize(self, width: int, height: int) -> None:
    #     """Resize the object's frames.

    #     Args:
    #         width (int): the new width of the object's frames.
    #         height (int): the new height of the object's frames.
    #     """
    #     self.frames = [
    #         pygame.transform.scale(frame, (width, height)) for frame in self.frames
    #     ]

    # def draw(
    #     self, x: int, y: int, surface: pygame.Surface, camera: tuple[int, int]
    # ) -> None:
    #     self._image = self.frames[self.current_frame]
    #     return super().draw(x, y, surface, camera)
