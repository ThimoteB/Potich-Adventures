""" Page for selecting the number of players """
import pygame


class PlayersPage:
    """This class is used to create the players page."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.player_count_options = [
            "2 Players",
            "3 Players",
            "4 Players",
        ]  # Options de nombre de joueurs
        self.selected_player_count = 0  # Choix actuellement sélectionné

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
