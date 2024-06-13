""" This module is used to create the game info."""

import pygame


class GameInfo(pygame.sprite.Sprite):
    """This class is used to create the game info."""

    def __init__(self, screen, black_width: int, gray_with: int, height: int):
        """This function is used to initialize the game info.

        Args:
            screen (pygame.surface): represents the screen
            width (int): represents the width of the game info
            height (int): represents the height of the game info
        """
        super().__init__()
        self.font = pygame.font.Font(None, 48)
        self.color = (255, 255, 255)
        self.current_player = "Joueur 1"
        self.text = self.font.render(self.current_player, True, (self.color))
        self.text_rect = self.text.get_rect()
        # Centre le texte sur la position X  de la black zone
        self.text_rect.center = (
            screen.get_width() - black_width - gray_with + black_width / 2,
            height,
        )

    def draw_gameinfo(self, screen: pygame.surface):
        """This function is used to draw the game info.

        Args:
            screen (pygame.surface): represents the screen
        """
        # REFRESH THE TEXT
        self.text = self.font.render(self.current_player, True, (self.color))
        screen.blit(self.text, self.text_rect)
