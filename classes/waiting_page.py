""" Page for the credits of the game """

import pygame
from game_constants.consts import PORT


class WaitingPage:
    """This class is used to display the waiting for host."""

    def __init__(self, screen, ip):
        self.screen = screen
        self.font = pygame.font.Font(None, 64)
        self.waiting_text = [
            f"Waiting for host at {ip}:{PORT}...",
        ]

    def draw(self):
        """This function is used to draw the credits page."""
        self.screen.fill((0, 0, 0))

        space = 50

        total_text_height = len(self.waiting_text) * space
        y = (self.screen.get_height() - total_text_height) // 2

        for line in self.waiting_text:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += space
