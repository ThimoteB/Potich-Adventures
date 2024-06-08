""" Page for selecting either online or solo """
import pygame


class GamemodePage:
    """This class is used to create the game mode selection page."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.gamemode_options = [
            "Solo",
            "Online"
        ]  # Game mode options
        self.selected_gamemode = 0  # Choix actuellement sélectionné

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
