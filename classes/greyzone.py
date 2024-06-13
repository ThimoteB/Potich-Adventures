""" This module is used to create the grey zone which is the zone to open the tab. """

import logging

import pygame

log = logging.getLogger(__name__)


class GreyZone(pygame.sprite.Sprite):
    """This class is used to create the grey zone which is the zone to open the tab.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(self, screen: pygame.sprite, width: int, height: int):
        """This function is used to initialize the grey zone.

        Args:
            screen (pygame.sprite): represents the screen
            width (int): represents the width of the grey zone
            height (int): represents the height of the grey zone
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen.get_width() - width, 0)
        self.color = (192, 192, 192)
        self.image.fill(self.color)
        self.visible = True
        self.black_open = False

    def draw(self, screen: pygame.sprite):
        """This function is used to draw the grey zone.

        Args:
            screen (pygame.sprite): represents the screen
        """
        if self.visible:
            screen.blit(self.image, self.rect)
            if not self.black_open:
                triangle_pos = (self.rect.centerx + 10, self.rect.centery)
                triangle_points = [
                    (triangle_pos[0], triangle_pos[1] - 25),
                    (triangle_pos[0], triangle_pos[1] + 25),
                    (triangle_pos[0] - 25, triangle_pos[1]),
                ]
                pygame.draw.polygon(screen, (0, 0, 0), triangle_points)
            else:
                triangle_pos = (self.rect.centerx - 10, self.rect.centery)
                triangle_points = [
                    (triangle_pos[0], triangle_pos[1] - 25),
                    (triangle_pos[0], triangle_pos[1] + 25),
                    (triangle_pos[0] + 25, triangle_pos[1]),
                ]
                pygame.draw.polygon(screen, (0, 0, 0), triangle_points)

    def on_click(self, mouse_pos: tuple):
        """This function is used to check if the grey zone is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse

        Returns:
            bool : True if the grey zone is clicked, False otherwise
        """
        if self.rect.collidepoint(mouse_pos):
            log.debug("Grey zone clicked!")
            self.black_open = not self.black_open
            return True
