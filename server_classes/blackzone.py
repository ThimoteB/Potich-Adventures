""" This module is used to create the black zone which is the hidden zone of the tab. """
import logging

import pygame

log = logging.getLogger(__name__)


class BlackZone(pygame.sprite.Sprite):
    """This class is used to create the black zone which is the hidden zone of the tab.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(
        self, screen: pygame.surface, width: int, height: int, grey_width: int
    ):
        """This function is used to initialize the black zone.

        Args:
            screen (pygame.surface): represents the screen
            width (int): represents the width of the black zone
            height (int): represents the height of the black zone
            grey_width (int): represents the width of the grey zone
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen.get_width() - width - grey_width, 0)
        self.color = (0, 0, 0)
        self.image.fill(self.color)
        self.visible = False

    def draw(self, screen):
        """This function is used to draw the black zone."""
        if self.visible:
            screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen: pygame.surface):
        """This function is used to draw the hitbox of the black zone."""
        pygame.draw.rect(screen, (105, 111, 116), self.rect, 5)

    def on_click(self, mouse_pos: tuple):
        """This function is used to check if the black zone is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse

        Returns:
            bool : True if the black zone is clicked, False otherwise
        """
        if self.rect.collidepoint(mouse_pos) and self.visible:
            log.debug("Black zone clicked!")
            return True
