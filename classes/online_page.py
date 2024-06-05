""" Page that show the lobby """
import pygame


class OnlinePage:
    """This class is used to show the lobby."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        
        self.text1 = [
            "Joueurs connectés:",
            "----------",
        ]

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

    def draw(self):
        """This function is used to draw the online players."""
        self.screen.fill((0, 0, 0))
        
        

        space = 50

        total_text_height = len(online_players) * space
        y = (self.screen.get_height() - total_text_height) // 2
        
        for line in self.text1:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += space