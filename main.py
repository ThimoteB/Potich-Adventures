"""Main client entry point"""

import logging
import socket
import json

import pygame
from rich.logging import RichHandler

from classes import (
    CreditsPage,
    PlayersPage,
    MapPage,
    RulePage,
    GamemodePage,
    WaitingPage,
    LobbyPage,
)
from game import Game
from client import Client
from game_constants.consts import PORT, PAYLOAD_SIZE

# program-wide logging formatter
root_logger = logging.getLogger()
print(root_logger.name)

console_handler = RichHandler()
root_logger.addHandler(console_handler)

file_handler = logging.FileHandler("client.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
root_logger.addHandler(file_handler)


root_logger.setLevel(logging.DEBUG)
root_logger.propagate = False
log = logging.getLogger(__name__)


class Main:
    """Main class for the game"""

    def __init__(self) -> None:
        pygame.init()  # pylint: disable=no-member
        pygame.font.init()
        # self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)  # pylint: disable=no-member
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

        self.host = ""
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []

    def draw_options(self, options, do_not_clear=False, manual_offset=0):
        """Draw the options on the screen"""
        if not do_not_clear:
            self.screen.fill(self.black)
        self.hitboxes = []

        screen_width, screen_height = self.screen.get_size()
        total_height = len(options) * 70
        y = ((screen_height - total_height) // 2) + manual_offset

        for i, option in enumerate(options):
            text = self.font.render(option, True, self.white)
            text_rect = text.get_rect(center=(screen_width // 2, y + i * 90))

            option_hitbox = text_rect.inflate(20, 20)
            self.hitboxes.append(option_hitbox)

            if i == self.selected_option:
                pygame.draw.rect(self.screen, self.white, option_hitbox, 2)

            self.screen.blit(text, text_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), option_hitbox, 2)

    def draw_input(self, kb_inut):
        """Draw an input box on the screen"""
        screen_width, screen_height = self.screen.get_size()
        total_height = 2 * 70
        y = (screen_height - total_height) // 2
        box_width = 200
        box_height = 64
        input_box = pygame.Rect(
            (screen_width // 2) - (box_width // 2),
            (screen_height // 2) - (box_height // 2),
            box_width,
            box_height,
        )
        color_inactive = self.white
        color_active = pygame.Color("red")
        color = color_inactive
        text = ""
        active = False

        sample_text = self.font.render(kb_inut, True, self.white)
        sample_rect = sample_text.get_rect(center=(screen_width // 2, y))

        done: bool = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    done = True
                if event.type == pygame.constants.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.constants.KEYDOWN:
                    if event.key == pygame.constants.K_ESCAPE:
                        return
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill(self.black)
            # Render the current text.
            txt_surface = self.font.render(text, True, self.white)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            # Blit the text.
            self.screen.blit(sample_text, sample_rect)
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            # Blit the input_box rect.
            pygame.draw.rect(self.screen, color, input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

    def remove_all_hitboxes(self):
        """Remove all hitboxes from the screen"""
        self.hitboxes = []

    def on_click(self, mouse_pos):
        """Check if the mouse is clicking on an option"""
        for i, hitbox in enumerate(self.hitboxes):
            if hitbox.collidepoint(mouse_pos):
                return i
        return -1

    def on_click_player(self, mouse_pos):
        """Check if the mouse is clicking on a player count"""
        for i, hitbox in enumerate(self.hitboxes):
            if hitbox.collidepoint(mouse_pos):
                self.player_count = i + 1
                return True
        return False

    def run(self):
        """Main game loop"""
        running = True
        tutorial_page = RulePage(self.screen)
        credits_page = CreditsPage(self.screen)
        players_page = PlayersPage(self.screen)
        map_page = MapPage(self.screen)
        gamemode_page = GamemodePage(self.screen)
        lobby_page = LobbyPage(self.screen)
        choosing_players = False
        choosing_map = False
        tutorial = False
        exiting_main_game = False
        choosing_gamemode = False
        online = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                    mouse_pos = pygame.mouse.get_pos()
                    if (
                        not choosing_players
                        and not choosing_map
                        and not tutorial
                        and not choosing_gamemode
                        and not online
                    ):
                        clicked_option_index = self.on_click(mouse_pos)
                        if clicked_option_index != -1:
                            selected_text = self.options[clicked_option_index]
                            if selected_text == "Tutorial":
                                tutorial = True
                                self.remove_all_hitboxes()
                                self.current_state = "Tutorial"
                            elif selected_text == "New Game":
                                choosing_gamemode = True
                                self.remove_all_hitboxes()
                                self.current_state = "Gamemode"
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

                        elif choosing_players:
                            if self.on_click_player(mouse_pos):
                                log.debug(self.player_count)
                                choosing_players = False
                                self.current_state = "Map"
                                choosing_map = True

                        elif choosing_gamemode:
                            clicked_option_index = self.on_click(mouse_pos)
                            if clicked_option_index != -1:
                                selected_text = gamemode_page.gamemode_options[
                                    clicked_option_index
                                ]
                                if selected_text == "Solo":  # normal game, no changes
                                    self.player_count = 1
                                    self.current_state = "Map"
                                    choosing_map = True
                                    choosing_gamemode = False
                                elif selected_text == "Online":
                                    self.player_count = 1
                                    self.current_state = "Online"
                                    online = True
                                    choosing_gamemode = False

                        elif online:
                            clicked_option_index = self.on_click(mouse_pos)
                            if clicked_option_index != -1:
                                selected_text = lobby_page.button_text[
                                    clicked_option_index
                                ]
                                if selected_text == "Start the game":
                                    self.current_state = "Start"

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
                    elif (
                        self.current_state == "Gamemode"
                    ):  # back to lobby when in online/offline page
                        self.current_state = "Lobby"
                    elif self.current_state == "Online":
                        self.current_state = "Gamemode"

            self.screen.fill(self.black)

            if self.current_state == "Lobby":
                self.draw_options(self.options)
            elif self.current_state == "Tutorial":
                tutorial_page.draw()
            elif self.current_state == "Credits":
                credits_page.draw()
            elif self.current_state == "Gamemode":  # Online/Offline page selection
                self.draw_options(gamemode_page.gamemode_options)
            elif self.current_state == "Players":
                self.draw_options(players_page.player_count_options)
            elif self.current_state == "Map":
                map_page.draw()
            elif self.current_state == "Main" and self.in_main_game:
                game = Game(self.player_count, self.map_chosen, self.fog)
                game.run()
                exiting_main_game = True
            elif self.current_state == "Online":
                self.host = self.draw_input("Enter the IP address of the server :")
                if not self.host:
                    online = False
                    self.current_state = "Gamemode"
                # try to reach the server
                WaitingPage(self.screen, self.host).draw()
                pygame.display.flip()

                result = self.sock.connect_ex((self.host, PORT))
                if result == 0:
                    log.debug("Server connection okay")
                    self.current_state = "OnlineLobby"
                    LobbyPage(self.screen).draw()
                else:
                    log.warning("Connection failed")

            # Connection etablished : waiting for other players
            elif self.current_state == "OnlineLobby":
                # wait for the server to send the number of players
                self.sock.setblocking(False)
                try:
                    data = self.sock.recv(PAYLOAD_SIZE)
                    data = json.loads(data.decode())
                    log.debug(data)
                    self.players = []
                    for player in data["players"]:
                        self.players.append((player[0], player[1]))
                    if data["start"]:
                        self.current_state = "Start"
                except BlockingIOError:
                    pass
                self.sock.setblocking(True)
                lobby_page.draw(self.players)
                self.draw_options(
                    [lobby_page.button_text], True, 100 + 64 * len(self.players)
                )
                pygame.display.flip()

            elif self.current_state == "Start":
                log.info("Starting the game")
                # TODO: start the game
                game = Client(self.sock)
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
