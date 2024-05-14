import logging

import pygame
from rich.logging import RichHandler

from classes import CreditsPage, PlayersPage, MapPage, RulePage
from game import Game

# program-wide logging formatter
root_logger = logging.getLogger()

handler = RichHandler()
root_logger.addHandler(handler)

root_logger.setLevel(logging.DEBUG)

root_logger.propagate = False

log = logging.getLogger(__name__)


class Main:
    def __init__(self) -> None:
        pygame.init()  # pylint: disable=no-member
        pygame.font.init()
        # self.screen = pygame.display.set_mode(
        #     flags=pygame.FULLSCREEN  # pylint: disable=no-member
        # )  # pylint: disable=no-member
        self.screen = pygame.display.set_mode((1600, 1000))
        self.clock = pygame.time.Clock()

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.font_size = 64
        self.font = pygame.font.Font(None, self.font_size)

        self.options = ["New Game", "Tutorial", "Credits", "Quit"]
        self.selected_option = -1

        self.hitboxes = []
        self.current_state = "Lobby"
        self.player_count = 0
        self.in_main_game = False
        self.map_chosen = None
        self.fog = False

    def draw_options(self, options):
        self.screen.fill(self.black)
        self.hitboxes = []

        screen_width, screen_height = self.screen.get_size()
        total_height = len(options) * 70
        y = (screen_height - total_height) // 2

        for i, option in enumerate(options):
            text = self.font.render(option, True, self.white)
            text_rect = text.get_rect(center=(screen_width // 2, y + i * 90))

            option_hitbox = text_rect.inflate(20, 20)
            self.hitboxes.append(option_hitbox)

            if i == self.selected_option:
                pygame.draw.rect(self.screen, self.white, option_hitbox, 2)

            self.screen.blit(text, text_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), option_hitbox, 2)

    def remove_all_hitboxes(self):
        self.hitboxes = []

    def on_click(self, mouse_pos):
        for i, hitbox in enumerate(self.hitboxes):
            if hitbox.collidepoint(mouse_pos):
                return i
        return -1

    def on_click_player(self, mouse_pos):
        for i, hitbox in enumerate(self.hitboxes):
            if hitbox.collidepoint(mouse_pos):
                self.player_count = i + 1
                return True
        return False

    def run(self):
        running = True
        tutorial_page = RulePage(self.screen)
        credits_page = CreditsPage(self.screen)
        players_page = PlayersPage(self.screen)
        map_page = MapPage(self.screen)
        choosing_players = False
        choosing_map = False
        tutorial = False
        exiting_main_game = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                    mouse_pos = pygame.mouse.get_pos()
                    if not choosing_players and not choosing_map and not tutorial:
                        clicked_option_index = self.on_click(mouse_pos)
                        if clicked_option_index != -1:
                            selected_text = self.options[clicked_option_index]
                            if selected_text == "Tutorial":
                                tutorial = True
                                self.remove_all_hitboxes()
                                self.current_state = "Tutorial"
                            elif selected_text == "New Game":
                                choosing_players = True
                                self.remove_all_hitboxes()
                                self.current_state = "Players"
                            elif selected_text == "Credits":
                                self.current_state = "Credits"
                                self.remove_all_hitboxes()
                            elif selected_text == "Quit":
                                running = False
                    else:
                        if choosing_map:
                            if map_page.on_click(mouse_pos):
                                self.map_chosen = map_page.return_map()
                                self.fog = map_page.return_fog()
                                choosing_map = False
                                self.current_state = "Main"
                                self.in_main_game = True
                            if map_page.on_click_random(mouse_pos):
                                self.map_chosen, self.fog = map_page.handle_random()
                                choosing_map = False
                                self.current_state = "Main"
                                self.in_main_game = True
                            if map_page.on_click_fog(mouse_pos):
                                map_page.handle_fog()
                        elif tutorial:
                            tutorial_page.on_click(mouse_pos)
                            print("TUTO CLICKED")

                        elif choosing_players:
                            if self.on_click_player(mouse_pos):
                                log.debug(self.player_count)
                                choosing_players = False
                                self.current_state = "Map"
                                choosing_map = True

                elif (
                    event.type == pygame.KEYDOWN  # pylint: disable=no-member
                    and event.key == pygame.K_ESCAPE  # pylint: disable=no-member
                ):  # pylint: disable=no-member
                    if self.current_state == "Credits":
                        self.current_state = "Lobby"
                    elif choosing_players:
                        choosing_players = False
                        self.current_state = "Lobby"
                    elif choosing_map:
                        choosing_map = False
                        choosing_players = True
                        self.current_state = "Players"
                    elif self.current_state == "Tutorial":
                        tutorial = False
                        self.current_state = "Lobby"

            self.screen.fill(self.black)

            if self.current_state == "Lobby":
                self.draw_options(self.options)
            elif self.current_state == "Tutorial":
                tutorial_page.draw()
            elif self.current_state == "Credits":
                credits_page.draw()
            elif self.current_state == "Players":
                self.draw_options(players_page.player_count_options)
            elif self.current_state == "Map":
                map_page.draw()
            elif self.current_state == "Main" and self.in_main_game:
                game = Game(self.player_count, self.map_chosen, self.fog)
                game.run()
                exiting_main_game = True

            if exiting_main_game:
                pygame.time.delay(1000)  # Wait 1 second before going back to the lobby
                self.in_main_game = False
                exiting_main_game = False
                self.current_state = "Lobby"

            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    main = Main()
    main.run()
