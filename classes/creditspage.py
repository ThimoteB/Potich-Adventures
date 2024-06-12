""" Page for the credits of the game """

import pygame


class CreditsPage:
    """This class is used to create the credits page."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.credits_text = [
            "Crédits:",
            "----------",
            "Bois Thimoté:",
            "Développeur",
            "Game Designer",
            "----------",
            "Prokopowicz Colin:",
            "Développeur",
            "Artiste",
            "Game Designer",
            "----------",
            "Lasagne Celian:",
            "Network Engineer",
            "----------",
            "analogStudios_:",
            "Tileset designer",
            "----------",
            "rawpixel on Freepick",
            "Fog texture",
            "----------",
            "Orange Cat By NoelaniEternal",
        ]

    def draw(self):
        """This function is used to draw the credits page."""
        self.screen.fill((0, 0, 0))

        space = 50

        total_text_height = len(self.credits_text) * space
        y = (self.screen.get_height() - total_text_height) // 2

        for line in self.credits_text:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += space
