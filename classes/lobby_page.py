""" Page for the credits of the game """
import pygame


class LobbyPage:
    """This class is used to display the lobby."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 64)
        self.button_text = "Start the game"
        self.waiting_text = [
            'Connected players :',
        ]

    def draw(self, players:list=[]):
        """This function is used to draw the lobby."""
        self.screen.fill((0, 0, 0))

        space = 50

        total_text_height = len(self.waiting_text) * space
        y = (self.screen.get_height() - total_text_height) // 2

        for line in self.waiting_text:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += space

        for player in players:
            text = self.font.render(f'{player[0]}:{player[1]}', True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += space
        
        # start button
        hitboxes = []

        screen_width, screen_height = self.screen.get_size()
        total_height = 70
        y = (screen_height - total_height) // 2

        text = self.font.render(self.button_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, y * 90))

        option_hitbox = text_rect.inflate(20, 20)
        hitboxes.append(option_hitbox)

        pygame.draw.rect(self.screen, (255, 255, 255), option_hitbox, 2)

        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 0, 0), option_hitbox, 2)