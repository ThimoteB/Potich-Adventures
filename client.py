""" File containing the main loop of the game """

import json
import logging
import socket
from time import sleep

import pygame  # pylint: disable=import-error

from classes import Board, Camera, Card, Enemy, Key, Pawn, Tab
from classes.card import *  # pylint: disable=unused-wildcard-import,wildcard-import
from classes.key import *  # pylint: disable=unused-wildcard-import,wildcard-import
from classes.map_object import MapCard, MapKey
from game_constants.consts import GRAPHICAL_TILE_SIZE, TICK_RATE, PAYLOAD_SIZE
from moves import *  # Import all the moves # pylint: disable=unused-wildcard-import,wildcard-import

log = logging.getLogger(__name__)

# Parce que on a défini une globale en dessous :)
card_selected: Card = None
highlighted_cells: list = []


class Client:
    """
    This class is used to create the main loop of the game.
    """

    def __init__(self, sock: socket.socket, fog=False):
        self.sock: socket.socket = sock
        self.sock.setblocking(False)
        self.data_out: dict = {
            "skip": False,
            "selected_card": None,  # assigned with the card_selected variable in the main loop
            "selected_cell": [None, None],
        }
        self.data_in: dict = {}
        """Data received from the server"""

        pygame.init()  # pylint: disable=no-member

        self.recv_data(blocking=True)
        self.player_number = self.data_in["player_number"]

        self.player_count = self.data_in["player_count"]
        self.map_chosen = self.data_in["map"]
        log.debug("Map chosen: %s", self.map_chosen)

        # self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)  # pylint: disable=no-member
        self.screen = pygame.display.set_mode((1600, 900))  # pylint: disable=no-member
        self.rect_fullscreen = pygame.Rect(
            0, 0, self.screen.get_width(), self.screen.get_height()
        )
        self.clock = pygame.time.Clock()
        self.camera = self.init_camera(self.data_in["map"])
        self.camera.set_bounds(self.screen.get_width(), self.screen.get_height())
        self.board = Board.from_tmx(
            tmx_file="maps/" + self.map_chosen,
            camera=self.camera,
            rect=False,
            card_map_list=self.data_in["card_map_list"],
            key_map_list=self.data_in["key_map_list"],
        )
        # TODO: edit board class to load cards and keys
        self.board.resize_tiles(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)
        self.tab = Tab(self.screen, 50, self.screen.get_height(), 50)
        self.tab.game_info.current_player = "Joueur " + str(self.player_number)
        self.init_game_elements(self.data_in["map"])
        self.fog = fog
        self.load_fog_image()
        self.init_fog_cells()
        self.highlighted_cells = []

    def send_data(self) -> bool:
        """This method send the data in the slef.data attribute to the server

        Returns:
            bool: False if the send fail
        """
        try:
            data: str = json.dumps(self.data_out)
            self.sock.sendall(data.encode())
            log.debug("Sent: %s", data)
            return True
        except BlockingIOError:
            return False

    def recv_data(self, blocking=False) -> bool:
        """This method receive data from the server and store it in the self.data_in attribute

        params:
            blocking (bool): if the receive should be blocking or not

        Returns:
            bool: False if the receive fail
        """
        self.sock.setblocking(blocking)
        try:
            data: bytes = self.sock.recv(PAYLOAD_SIZE)
            if not data:
                return False
            self.data_in = json.loads(data.decode())
            log.debug("Received: %s", self.data_in)
            self.sock.setblocking(False)
            return True
        except BlockingIOError:
            return False

    def end_game(self):
        """
        This function is used to end the game.
        """
        self.sock.close()
        font = pygame.font.SysFont("arial", 100)
        text = font.render("You Win", True, (0, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (
            self.screen.get_width() // 2,
            self.screen.get_height() // 2,
        )
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        sleep(5)

    def load_fog_image(self):
        """
        This function is used to load the fog image.
        """
        self.fog_image = pygame.image.load("images/fog.jpeg")
        self.fog_image = pygame.transform.scale(
            self.fog_image, (GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)
        )

    def init_fog_cells(self):
        """
        This function is used to initialize the fog cells.
        """
        self.list_fog_cases = [cell for row in self.board.cells for cell in row]
        self.fog_range = 3

    def draw_fog(self, camera_offset: tuple[int, int]):
        """This function is used to draw the fog.

        Args:
            camera_offset (tuple[int, int]): camera offset
        """
        for case in self.list_fog_cases:
            self.screen.blit(
                self.fog_image,
                (
                    case.x * GRAPHICAL_TILE_SIZE + camera_offset[0],
                    case.y * GRAPHICAL_TILE_SIZE + camera_offset[1],
                ),
            )

    # TODO: not used ?
    def get_nearby_cells(self, pawn: Pawn, distance: int):
        """This function is used to get the nearby cells depending on the distance argument.

        Args:
            pawn (Pawn): pawn object
            distance (int): distance

        Returns:
            list: list of nearby cells
        """
        pawn_y, pawn_x = self.get_coord_pawn(pawn)
        around_cases = []

        for row in self.board.cells:
            for cell in row:
                # Calcul of the distance between the pawn and the cell
                cell_y, cell_x = cell.y, cell.x
                distance_to_cell = (
                    (cell_x - pawn_x) ** 2 + (cell_y - pawn_y) ** 2
                ) ** 0.5

                # Verif if the cell is in the range of the pawn
                if distance_to_cell <= distance:
                    around_cases.append(cell)

        return around_cases

    def init_camera(self, mapchoose: str):
        """This function is used to initialize the camera.

        Args:
            mapchoose (str): map chosen by the player

        Returns:
            Camera: camera object
        """
        camera_positions = {
            "map1.tmx": (450, 1300),
            "map2.tmx": (750, 900),
            "map3.tmx": (0, 800),
            "map4.tmx": (1400, 700),
            "map5.tmx": (700, 780),
            "map_courte.tmx": (560, 600),
        }
        return Camera(*camera_positions.get(mapchoose, (0, 0)))

    def init_game_elements(self, mapchoose: str):
        """This function is used to initialize the game elements.

        Args:
            mapchoose (str): map chosen by the player
        """

        self.list_pawns = []
        self.list_enemies = []
        self.pawn1 = Pawn(
            pygame.image.load("images/gamesprites/pawn/char_18.png").convert_alpha(),
            "Gork",
            100,
            20,
        )
        self.pawn2 = Pawn(
            pygame.image.load("images/gamesprites/pawn/char_32.png").convert_alpha(),
            "Nano",
            100,
            20,
        )
        self.pawn3 = Pawn(
            pygame.image.load("images/gamesprites/pawn/char_47.png").convert_alpha(),
            "Sylphe",
            100,
            20,
        )
        self.pawn4 = Pawn(
            pygame.image.load("images/gamesprites/pawn/char_44.png").convert_alpha(),
            "Poticha",
            100,
            20,
        )

        self.enemy1 = Enemy(
            pygame.image.load("images/gamesprites/pawn/char_35.png").convert_alpha(),
            "Squelette",
            100,
            20,
            "Neutral",
            ia=True,
        )
        self.enemy2 = Enemy(
            pygame.image.load("images/gamesprites/pawn/char_28.png").convert_alpha(),
            "Zombie",
            100,
            20,
            "Fire",
            ia=True,
        )
        self.enemy3 = Enemy(
            pygame.image.load("images/gamesprites/pawn/char_33.png").convert_alpha(),
            "Golem de Terre",
            100,
            20,
            "Grass",
            ia=True,
        )
        self.enemy4 = Enemy(
            pygame.image.load("images/gamesprites/pawn/char_26.png").convert_alpha(),
            "Pieuvre",
            100,
            20,
            "Water",
            ia=True,
        )

        pawn_positions = {
            "map1.tmx": [(60, 36), (63, 41), (59, 45), (56, 41)],
            "map2.tmx": [(47, 50), (50, 53), (45, 57), (42, 53)],
            "map3.tmx": [(49, 8), (47, 12), (42, 12), (40, 8)],
            "map4.tmx": [(48, 75), (46, 81), (35, 83), (37, 78)],
            "map5.tmx": [(42, 42), (46, 49), (42, 54), (37, 50)],
            "map_courte.tmx": [(38, 46), (39, 45), (38, 44), (37, 45)],
        }

        enemy_positions = {
            "map1.tmx": [(81, 81), (44, 89), (15, 50), (73, 8)],
            "map2.tmx": [(66, 75), (28, 76), (32, 25), (65, 32)],
            "map3.tmx": [(92, 72), (63, 69), (30, 72), (8, 53)],
            "map4.tmx": [(99, 86), (91, 76), (68, 21), (16, 32)],
            "map5.tmx": [(93, 23), (78, 96), (14, 81), (24, 5)],
            "map_courte.tmx": [(46, 50), (34, 35), (26, 46)],
        }

        # TODO: append pawn and enemy received from server to the list
        self.list_pawns.append(self.pawn1)
        self.list_pawns.append(self.pawn2)
        self.list_pawns.append(self.pawn3)
        self.list_pawns.append(self.pawn4)

        self.list_enemies.append(self.enemy1)
        self.list_enemies.append(self.enemy2)
        self.list_enemies.append(self.enemy3)
        if not mapchoose == "map_courte.tmx":
            self.list_enemies.append(self.enemy4)

        for i, pawn in enumerate(self.list_pawns):
            y, x = pawn_positions[mapchoose][i]
            self.board.cells[y][x].add_pawn(pawn)

        for i, enemy in enumerate(self.list_enemies):
            y, x = enemy_positions[mapchoose][i]
            self.board.cells[y][x].add_pawn(enemy)

        self.init_cards_slots()
        self.init_key_slots()
        self.card_selected = None
        self.pawn_selected = None

    def init_cards_slots(self):
        """This function is used to initialize the cards slots."""
        # pylint: disable=attribute-defined-outside-init
        self.group_slots_card = [
            self.tab.top_left_slot,
            self.tab.top_right_slot,
            self.tab.bottom_left_slot,
            self.tab.bottom_right_slot,
        ]
        self.card_croix: Card = card_croix
        self.card_lightning: Card = card_lightning
        self.card_horloge: Card = card_horloge
        self.card_fontaine: Card = card_fontaine
        self.card_plume: Card = card_plume
        self.card_up_1: Card = card_up_1
        self.card_up_2: Card = card_up_2
        self.card_down_1: Card = card_down_1
        self.card_down_2: Card = card_down_2
        self.card_left_1: Card = card_left_1
        self.card_left_2: Card = card_left_2
        self.card_right_1: Card = card_right_1
        self.card_right_2: Card = card_right_2
        self.card_supreme: Card = card_supreme

        self.card_list: list[Card] = [
            card_croix,
            card_lightning,
            card_horloge,
            card_fontaine,
            card_plume,
            card_up_1,
            card_up_2,
            card_down_1,
            card_down_2,
            card_left_1,
            card_left_2,
            card_right_1,
            card_right_2,
            card_supreme,
        ]

        for i, card in enumerate(self.data_in["cards"]):
            for c in self.card_list:
                if c.get_name == card:
                    self.group_slots_card[i].add_item(c)
                    break

        # pylint: enable=attribute-defined-outside-init

    def update_cards(self):
        """This function is used to update the cards."""
        for i in range(4):
            self.group_slots_card[i].reset_item()
        for i, card in enumerate(self.data_in["cards"]):
            for c in self.card_list:
                if c.get_name == card:
                    self.group_slots_card[i].add_item(c)
                    break

    def update_keys(self):
        """This function is used to update the keys."""
        for i in range(4):
            self.group_slots_key[i].reset_item()
        for i, key in enumerate(self.data_in["keys"]):
            match key:
                case "red key":
                    self.group_slots_key[i].add_item(self.red_key)
                case "blue key":
                    self.group_slots_key[i].add_item(self.blue_key)
                case "green key":
                    self.group_slots_key[i].add_item(self.green_key)
                case "yellow key":
                    self.group_slots_key[i].add_item(self.yellow_key)

    def init_key_slots(self):
        """This function is used to initialize the key slots."""
        # pylint: disable=attribute-defined-outside-init
        self.group_slots_key = [
            self.tab.first_key_slot,
            self.tab.second_key_slot,
            self.tab.third_key_slot,
            self.tab.fourth_key_slot,
        ]
        # pylint: enable=attribute-defined-outside-init

        key_slot_width: int = 80
        key_slot_height: int = 80
        self.red_key = Key(
            "images/red key.png", key_slot_width, key_slot_height, "red key"
        )
        self.blue_key = Key(
            "images/blue key.png", key_slot_width, key_slot_height, "blue key"
        )
        self.green_key = Key(
            "images/green key.png", key_slot_width, key_slot_height, "green key"
        )
        self.yellow_key = Key(
            "images/yellow key.png", key_slot_width, key_slot_height, "yellow key"
        )

    def add_key_slot(self, key: Key):
        """This function is used to add a key slot.

        Args:
            key (Key): key object
        """
        for slot in self.group_slots_key:
            if slot.item is None:
                slot.add_item(key)
                break

    def is_key_slot_full(self):
        """This function is used to check if the key slot is full.

        Returns:
            bool: True if the key slot is full, False otherwise
        """
        return all(slot.item is not None for slot in self.group_slots_key)

    def handle_input_cam(self):
        """This function is used to handle the input of the camera."""
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:  # pylint: disable=no-member
            dx = -20
        if keys[pygame.K_RIGHT]:  # pylint: disable=no-member
            dx = 20
        if keys[pygame.K_UP]:  # pylint: disable=no-member
            dy = -20
        if keys[pygame.K_DOWN]:  # pylint: disable=no-member
            dy = 20

        self.camera.move(dx, dy)

    # TODO: server process function !!!
    # def move_check_key_and_card(
    #     self, pawn_selected: Pawn, new_y: int, new_x: int, pawn_y: int, pawn_x: int
    # ):
    #     """This function is used to move the pawn, check if there is a key or a card on the cell.

    #     Args:
    #         pawn_selected (Pawn): pawn object
    #         new_y (int): New y coordinate
    #         new_x (int): New x coordinate
    #         pawn_y (int): current y coordinate
    #         pawn_x (int): current x coordinate
    #     """
    #     if isinstance(self.board.cells[new_y][new_x].game_object, MapCard or Card):
    #         if len(self.queue.queue[0].cards) < 4:
    #             self.queue.queue[0].add_card(
    #                 self.board.cells[new_y][new_x].game_object.card
    #             )
    #             # ex : Le joueur 1 a récupéré la carte croix
    #             self.tab.log_event.write_logfile(
    #                 "log_event.txt",
    #                 "Le joueur %d a récupéré la carte %s "
    #                 % (
    #                     self.queue.queue[0].number,
    #                     self.board.cells[new_y][new_x].game_object.card.name,
    #                 ),
    #             )
    #         else:
    #             self.tab.log_event.write_logfile(
    #                 "log_event.txt",
    #                 "Le joueur %d a déchiré la carte %s "
    #                 % (
    #                     self.queue.queue[0].number,
    #                     self.board.cells[new_y][new_x].game_object.card.name,
    #                 ),
    #             )

    #     log.debug(isinstance(self.board.cells[new_y][new_x].game_object, MapKey or Key))
    #     if isinstance(self.board.cells[new_y][new_x].game_object, MapKey or Key):
    #         self.add_key_slot(self.board.cells[new_y][new_x].game_object.key)
    #         # ex : Le joueur 1 a récupéré la clé rouge
    #         self.tab.log_event.write_logfile(
    #             "log_event.txt",
    #             "Le joueur %d a récupéré la clé %s "
    #             % (
    #                 self.queue.queue[0].number,
    #                 self.board.cells[new_y][new_x].game_object.key.name,
    #             ),
    #         )
    #     self.board.move_or_attack(pawn_selected, new_y, new_x, (pawn_y, pawn_x))

    def clicked_cell(self, mouse_pos: tuple[int, int]):
        """This function is used to get the clicked cell.

        Args:
            mouse_pos (tuple[int, int]): mouse position

        Returns:
            Cell: cell object
        """
        mouse_x, mouse_y = mouse_pos
        map_x = (mouse_x + self.camera.x) // GRAPHICAL_TILE_SIZE
        map_y = (mouse_y + self.camera.y) // GRAPHICAL_TILE_SIZE
        if 0 <= map_x < self.board.width and 0 <= map_y < self.board.height:
            clicked_cell = self.board.cells[map_y][map_x]
            log.debug("Clicked cell: (%d, %d)", clicked_cell.y, clicked_cell.x)
            if isinstance(clicked_cell.game_object, MapCard or Card):
                log.debug("Card: %s", clicked_cell.game_object.card.name)
            elif isinstance(clicked_cell.game_object, MapKey or Key):
                log.debug("Key: %s", clicked_cell.game_object.key.name)
            else:
                log.debug("GAME OBJECT: %s", clicked_cell.game_object)
        return clicked_cell

    def select_pawn(self, cell: object):
        """This function is used to select a pawn.

        Args:
            cell (Cell: cell object on which the pawn is located

        Returns:
            Pawn: pawn object
        """
        if cell.game_object:
            pawn_selected = cell.game_object
            return pawn_selected
        return None

    def unhilight(self):
        """This function is used to unhighlight the cells."""
        for row in self.board.cells:
            for cell in row:
                cell.unhighlight()

    def get_coord_pawn(self, pawn: Pawn):
        """This function is used to get the coordinates of the pawn.

        Args:
            pawn (Pawn): pawn object

        Returns:
            tuple[int, int]: tuple of coordinates
        """
        for row in self.board.cells:
            for cell in row:
                if cell.game_object == pawn:
                    return cell.y, cell.x

    def handle_card_selection(self, index: int) -> Card:
        """This function is used to handle the card selection.

        Args:
            index (int): index of the card

        Returns:
            Card: card object
        """
        global card_selected, highlighted_cells
        previous_card_selected = self.card_selected
        card_selected = self.tab.handle_click_shortcut_cards(index)

        # Check if the same card is re-selected
        if card_selected == previous_card_selected:
            self.highlighted_cells = []
            card_selected = None
            self.unhilight()
        elif card_selected:
            self.unhilight()
            self.highlighted_cells = []

        return card_selected

    def run(self):
        """This function is used to run the game."""

        # Initialize variables
        frame_id = 0
        card_selected: Card = None
        pawn_selected = None
        highlighted_cells = []

        # Main loop
        while True:
            self.recv_data()

            # Update the map
            self.board.update_elements(
                self.data_in["elements"], self.data_in["possible_moves"]
            )

            # Update cards
            self.update_cards()
            self.update_keys()

            # Managements of the frames
            self.clock.tick(TICK_RATE)
            frame_id += 1
            self.board.tick(frame_id)

            # Draw the board
            self.screen.fill((0, 0, 0))
            self.board.draw(self.screen)

            # Draw the fog if activated
            if self.fog:
                camera_offset = (-self.camera.x, -self.camera.y)
                self.draw_fog(camera_offset)

            # Draw the tab
            self.tab.draw(self.screen)
            if self.tab.is_expanded:
                self.tab.black_zone.draw_hitbox(self.screen)

            # End game if all the key slots are full
            if self.is_key_slot_full():
                self.end_game()
                break

            if self.data_in["current_player"] == self.player_number:
                self.tab.game_info.current_player = "C'est votre tour"

            else:
                self.tab.game_info.current_player = (
                    f" Tour du joueur {self.data_in['current_player'] + 1} "
                )

            for event in pygame.event.get():
                # TODO: client side event management
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    return
                # Shortcuts for opening and closing the tab
                elif pygame.key.get_pressed()[pygame.K_TAB]:
                    self.tab.gray_zone.black_open = not self.tab.gray_zone.black_open
                    self.tab.toggle_expand()

                elif event.type == pygame.KEYDOWN:
                    # action only if the current player is the client
                    if self.data_in["current_player"] == self.player_number:
                        key_pressed = pygame.key.get_pressed()
                        if key_pressed[pygame.K_1]:
                            card_selected = self.handle_card_selection(0)
                        elif key_pressed[pygame.K_2]:
                            card_selected = self.handle_card_selection(1)
                        elif key_pressed[pygame.K_3]:
                            card_selected = self.handle_card_selection(2)
                        elif key_pressed[pygame.K_4]:
                            card_selected = self.handle_card_selection(3)

                        elif event.key == pygame.K_SPACE:  # pylint: disable=no-member
                            # If the player press space, the turn is skipped
                            self.tab.unselect_all_cards()
                            self.unhilight()
                            card_selected = None
                            pawn_selected = None
                            self.data_out["skip"] = True
                            self.data_out["selected_card"] = None
                            self.data_out["selected_cell"] = None
                            self.send_data()
                            self.data_out["skip"] = False
                        elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                            return

                # CLICKS
                elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                    # Only the current player can play
                    # Check if the click is on the tab ( for not clicking on the cell behind)
                    # Open or close the tab
                    if self.tab.gray_zone.on_click(pygame.mouse.get_pos()):
                        self.tab.handle_input(pygame.mouse.get_pos())

                    # Check if the click is on the black zone ( for not clicking on the cell behind)
                    # Detect if a card is selected or unselected
                    elif self.tab.black_zone.on_click(pygame.mouse.get_pos()):
                        # action only if the current player is the client
                        if self.data_in["current_player"] == self.player_number:
                            self.data_out["selected_cell"] = [None, None]
                            log.debug("Mouse click at %s", pygame.mouse.get_pos())
                            previous_card_selected = card_selected
                            card_selected = self.tab.handle_click(
                                pygame.mouse.get_pos()
                            )
                            # Check if the same card is re-selected
                            if card_selected == previous_card_selected:
                                highlighted_cells = []
                                card_selected = None
                                self.unhilight()
                                log.debug("Unselected card %s", previous_card_selected)
                                self.data_out["selected_card"] = None
                                self.send_data()
                                continue

                            if card_selected:
                                log.debug("Selected card: %s", card_selected.name)
                                self.unhilight()
                                highlighted_cells = []

                                # send the card
                                self.data_out["selected_card"] = card_selected.name
                                self.send_data()

                    # Case where the click is on the board
                    else:
                        # Only the current player can play
                        if self.data_in["current_player"] == self.player_number:
                            clicked_cell = self.clicked_cell(pygame.mouse.get_pos())
                            log.debug("Clicked cell: %s", clicked_cell)
                            self.data_out["selected_cell"] = [
                                clicked_cell.y,
                                clicked_cell.x,
                            ]
                            self.send_data()

            # Handle camera movement
            self.handle_input_cam()

            pygame.display.flip()


if __name__ == "__main__":
    # Can be used to test a single client connection
    from rich.logging import RichHandler

    root_logger = logging.getLogger()
    handler = RichHandler()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)
    root_logger.propagate = False
    log = logging.getLogger(__name__)

    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect_ex(("127.0.0.1", 44440))
    log.debug(sock.recv(PAYLOAD_SIZE).decode())

    game = Client(sock)
    game.run()
    pygame.quit()
