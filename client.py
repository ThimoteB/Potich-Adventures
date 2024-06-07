""" File containing the main loop of the game """

from queue import Queue
from time import sleep
import logging
import pygame  # pylint: disable=import-error
import socket, json

from game_constants.consts import TICK_RATE, GRAPHICAL_TILE_SIZE, SOUND
from classes import Tab, Board, Player, Card, Key, Camera, Pawn, Enemy, EndTurn
from classes.map_object import MapCard, MapKey
from moves import *  # Import all the moves # pylint: disable=unused-wildcard-import,wildcard-import
from classes.card import *  # pylint: disable=unused-wildcard-import,wildcard-import
from classes.key import *  # pylint: disable=unused-wildcard-import,wildcard-import


log = logging.getLogger(__name__)


class Client:
    """
    This class is used to create the main loop of the game.
    """

    def __init__(self, sock:socket.socket, player_count=2, mapchoose="map1.tmx", fog=False):
        self.sock:socket.socket = sock
        self.sock.setblocking(False)
        self.data_out:dict = {
            "skip": False,
            "selected_card": None, # assigned with the card_selected variable in the main loop
            "selected_cell": None
        }
        self.data_in:dict = {}
        """Data received from the server"""
        
        pygame.init()  # pylint: disable=no-member
        self.player_count = player_count
        # self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)  # pylint: disable=no-member
        self.screen = pygame.display.set_mode((1600, 900))  # pylint: disable=no-member
        self.rect_fullscreen = pygame.Rect(
            0, 0, self.screen.get_width(), self.screen.get_height()
        )
        self.clock = pygame.time.Clock()
        self.camera = self.init_camera(mapchoose)
        self.camera.set_bounds(self.screen.get_width(), self.screen.get_height())
        self.map_chosen = mapchoose
        self.board = Board.from_tmx("maps/" + self.map_chosen, self.camera, False)
        self.board.resize_tiles(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)
        self.tab = Tab(self.screen, 50, self.screen.get_height(), 50)
        self.init_game_elements(mapchoose)
        self.fog = fog
        self.load_fog_image()
        self.init_fog_cells()
    
    def send_data(self) -> bool:
        """This method send the data in the slef.data attribute to the server

        Returns:
            bool: False if the send fail
        """
        try:
            data:str = json.dumps(self.data_out)
            self.sock.sendall(data.encode())
            log.debug("Sent: %s", data)
            return True
        except:
            return False
    
    def reset_data(self):
        self.data_out["skip"] = False
        self.data_out["selected_card"] = None
        self.data_out["selected_cell"] = False
        

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
            ia=True,
        )
        self.enemy2 = Enemy(
            pygame.image.load("images/gamesprites/pawn/char_35.png").convert_alpha(),
            "Squelette",
            100,
            20,
            ia=True,
        )
        self.enemy3 = Enemy(
            pygame.image.load("images/gamesprites/pawn/char_35.png").convert_alpha(),
            "Squelette",
            100,
            20,
            ia=True,
        )
        self.enemy4 = Enemy(
            pygame.image.load("images/gamesprites/pawn/char_35.png").convert_alpha(),
            "Squelette",
            100,
            20,
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

        # TODO: the client does not need to know the queue
        # self.queue = Queue()
        for player in range(self.player_count):
            self.queue.put(Player(player + 1))
        self.queue.put(self.enemy1)
        self.queue.put(self.enemy2)
        self.queue.put(self.enemy3)
        if not mapchoose == "map_courte.tmx":
            self.queue.put(self.enemy4)
        self.queue.put(EndTurn())

        self.init_cards_slots()
        self.init_key_slots()
        self.card_selected = None
        self.pawn_selected = None

    
    def init_cards_slots(self):
        """This function is used to initialize the cards slots."""
        self.group_slots_card = [
            self.tab.top_left_slot,
            self.tab.top_right_slot,
            self.tab.bottom_left_slot,
            self.tab.bottom_right_slot,
        ]
        self.card_croix = card_croix
        self.card_lightning = card_lightning
        self.card_horloge = card_horloge
        self.card_fontaine = card_fontaine
        self.card_plume = card_plume
        self.card_up_1 = card_up_1
        self.card_up_2 = card_up_2
        self.card_down_1 = card_down_1
        self.card_down_2 = card_down_2
        self.card_left_1 = card_left_1
        self.card_left_2 = card_left_2
        self.card_right_1 = card_right_1
        self.card_right_2 = card_right_2
        self.card_supreme = card_supreme

        # match self.player_count:
        #     case 1:
        #         self.queue.queue[0].add_card(self.card_up_1)
        #         self.queue.queue[0].add_card(self.card_down_1)
        #         self.queue.queue[0].add_card(self.card_left_1)
        #         self.queue.queue[0].add_card(self.card_right_1)
        #     case 2:
        #         self.queue.queue[0].add_card(self.card_up_1)
        #         self.queue.queue[0].add_card(self.card_down_1)
        #         self.queue.queue[1].add_card(self.card_left_1)
        #         self.queue.queue[1].add_card(self.card_right_1)
        #     case 3:
        #         self.queue.queue[0].add_card(self.card_up_1)
        #         self.queue.queue[1].add_card(self.card_down_1)
        #         self.queue.queue[2].add_card(self.card_left_1)
        #         self.queue.queue[2].add_card(self.card_right_1)
        #     case 4:
        #         self.queue.queue[0].add_card(self.card_up_1)
        #         # self.queue.queue[0].add_card(self.card_supreme)
        #         self.queue.queue[0].add_card(self.card_plume)
        #         self.queue.queue[0].add_card(self.card_croix)
        #         self.queue.queue[1].add_card(self.card_down_1)
        #         self.queue.queue[2].add_card(self.card_left_1)
        #         self.queue.queue[3].add_card(self.card_right_1)

    def init_key_slots(self):
        """This function is used to initialize the key slots."""
        self.group_slots_key = [
            self.tab.first_key_slot,
            self.tab.second_key_slot,
            self.tab.third_key_slot,
            self.tab.fourth_key_slot,
        ]

    # TODO: no need to swap card for the client
    # def swap_card(self, queue: Queue):
    #     """This function is used to swap the cards depending on the player.

    #     Args:
    #         queue (Queue): queue object
    #     """
    #     for slot in self.group_slots_card:
    #         slot.reset_item()
    #     if isinstance(queue.queue[0], Player):
    #         for card in queue.queue[0].cards:
    #             self.group_slots_card[queue.queue[0].cards.index(card)].add_item(card)

    def swap_player(self, queue: Queue):
        """This function is used to swap the player.

        Args:
            queue (Queue): queue object
        """
        # TODO: maybe send a signal to all clients ?
        queue.put(queue.get())
        if isinstance(queue.queue[0], Player):
            self.tab.game_info.current_player = "Joueur " + str(queue.queue[0].number)
        else:
            self.tab.game_info.current_player = "Enemy"
        self.unhilight()
        self.tab.unselect_all_cards()

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

    # TODO: client only function
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

    def handle_card_selection(self, index: int):
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
        card_selected = None
        pawn_selected = None
        highlighted_cells = []

        # Main loop
        while True:
            # TODO: get data from server
            
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
            
            # TODO: server check
            # Case where the current element of the queue is an enemy
            # if isinstance(self.queue.queue[0], Enemy):
            #     if self.queue.queue[0].health <= 0:
            #         self.queue.get()
            #         continue
            #     self.board.move_enemy(self.queue.queue[0], self.player_count)
            #     self.swap_player(self.queue)
            #     continue

            # if isinstance(self.queue.queue[0], EndTurn):
            #     # Actions that happens at the end of a turn
            #     # TODO: keep this for the server
            #     self.swap_player(self.queue)

            #     # heal all the pawns that are on healing tiles
            #     # TODO: keep this for the server (and send a signal to the client to update the health of the pawns)
            #     for row in self.board.cells:
            #         for cell in row:
            #             if cell.game_object and isinstance(cell.game_object, Pawn):
            #                 if cell.is_heal_cell:
            #                     old_health = cell.game_object.health
            #                     cell.game_object.health = min(
            #                         cell.game_object.health + cell.heal_value, 100
            #                     )  # maximum 100 HP
            #                     if cell.game_object.health != old_health:
            #                         self.tab.log_event.write_logfile(
            #                             "log_event.txt",
            #                             "%s a été soigné de %d HP"
            #                             % (
            #                                 cell.game_object.name,
            #                                 cell.heal_value,
            #                             ),
            #                         )
            #                     if SOUND:
            #                         if cell.game_object.health != old_health:
            #                             heal_sound = pygame.mixer.Sound(
            #                                 "sounds/heal.mp3"
            #                             )
            #                             if cell.heal_value >= 10:
            #                                 heal_sound.play()
            #                             else:
            #                                 heal_sound.set_volume(0.3)
            #                                 heal_sound.play()
            #                         # TODO - spawn heart particles
            #     continue

            for event in pygame.event.get():
                # TODO: client side event management
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    return
                # Shortcuts for opening and closing the tab
                elif pygame.key.get_pressed()[pygame.K_TAB]:
                    self.tab.gray_zone.black_open = not self.tab.gray_zone.black_open
                    self.tab.toggle_expand()
                elif event.type == pygame.KEYDOWN:
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
                        # TODO: tell the server to skip the turn
                        # If the player press space, the turn is skipped
                        self.swap_player(self.queue)
                        self.tab.unselect_all_cards()
                        self.unhilight()
                        card_selected = None
                        pawn_selected = None
                    elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                        return

                # CLICKS
                elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                    # Check if the click is on the tab ( for not clicking on the cell behind)
                    # Open or close the tab
                    if self.tab.gray_zone.on_click(pygame.mouse.get_pos()):
                        self.tab.handle_input(pygame.mouse.get_pos())

                    # Check if the click is on the black zone ( for not clicking on the cell behind)
                    # Detect if a card is selected or unselected
                    elif self.tab.black_zone.on_click(pygame.mouse.get_pos()):
                        print(pygame.mouse.get_pos())
                        previous_card_selected = card_selected
                        card_selected = self.tab.handle_click(pygame.mouse.get_pos())
                        # Check if the same card is re-selected
                        if card_selected == previous_card_selected:
                            highlighted_cells = []
                            card_selected = None
                            self.unhilight()
                            continue

                        if card_selected:
                            self.unhilight()
                            highlighted_cells = []
                        
                        # add the selected card to the data to be sent when a pawn is clicked
                        self.data_out["selected_card"] = card_selected
                        self.send_data()

                    # Case where the click is on the board
                    else:
                        clicked_cell = self.clicked_cell(pygame.mouse.get_pos())
                        self.data_out["selected_cell"] = clicked_cell
                        self.send_data()
                        # clicked_cell_y, clicked_cell_x = clicked_cell.y, clicked_cell.x

                        # TODO: let the sever handle the click on the cell
                        # Check if the click is on a pawn for selecting it
                        # if clicked_cell.game_object and isinstance(
                        #     clicked_cell.game_object, Pawn
                        # ):
                        #     pawn_selected = self.select_pawn(clicked_cell)
                        #     highlighted_cells = []
                        #     self.unhilight()
                            # if pawn_selected and card_selected:
                                # possible_moves = self.board.highlight_possible_moves(
                                #     pawn_selected, card_selected
                                # )
                                # highlighted_cells = possible_moves
                                # let the calculation be done on the server
                                # TODO: highlight cells with server data

                        # TODO: keep this part of the code with the client cells received
                        # Search if the clicked cell is in the highlighted cells
                        # else:
                        #     if (clicked_cell_y, clicked_cell_x) in highlighted_cells:
                        #         pawn_y, pawn_x = self.get_coord_pawn(pawn_selected)
                        #         new_y, new_x = clicked_cell_y, clicked_cell_x

                        #         # Move the pawn on the new cell
                        #         self.move_check_key_and_card(
                        #             pawn_selected, new_y, new_x, pawn_y, pawn_x
                        #         )

                        #         # End of the turn
                        #         self.swap_player(self.queue)
                        #         # Reset All variables
                        #         self.tab.unselect_all_cards()
                        #         self.unhilight()
                        #         clicked_cell = None
                        #         card_selected = None
                        #         pawn_selected = None
            
            
            
            # TODO: receive the selected card and pawn from the client
            # TODO: send possible moves to the client and wait for the selected move or another card/pawn
            
            # Handle camera movement
            self.handle_input_cam()

            # Swap the card for the next player
            # self.swap_card(self.queue)

            pygame.display.flip()
            
            # TODO: render the player swap
            self.tab.game_info.current_player = "Joueur " + (self.data_in["current_player"]+1)


if __name__ == "__main__":
    pass