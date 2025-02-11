""" This file contains the board class that will be used to create the board and the cells."""

from __future__ import annotations

import random
import logging
import math
import pytmx
import pygame
from game_constants.consts import GRAPHICAL_TILE_SIZE
from .cell import Cell
from .map_object import Tile, AnimatedTile, MapKey, Pawn, Enemy, MapCard
from .camera import Camera
from .card import list_of_cards  # pylint: disable=wildcard-import
from .key import list_of_keys  # pylint: disable=wildcard-import
from .card import Card
from .key import Key

log = logging.getLogger(__name__)


class Board(pygame.sprite.Sprite):
    """This class is used to create the board and the cells.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(
        self,
        width: int,
        height: int,
        tile_width: int,
        tile_height: int,
        camera: Camera,
        rect: bool = False,
    ):
        """This function is used to initialize the board and the cells.

        Args:
            width (int): represents the width of the board
            height (int): represents the height of the board
            cell_width (int): represents the width of the cells
            cell_height (int): represents the height of the cells
            camera (object): represents the camera
        """
        self.width = width
        self.height = height
        self.tilewidth = tile_width
        self.tileheight = tile_height
        self.cells = [[None for _ in range(width)] for _ in range(height)]
        self.camera = camera
        self.rect = rect
        self.healing_tiles = []

    def get_coordinates_object(self, game_object: object) -> tuple[int, int]:
        """This function is used to get the coordinates of an object on the board.

        Args:
            game_object (object): represents the object

        Returns:
            tuple[int, int]: represents the coordinates of the object
        """
        for row in self.cells:
            for cell in row:
                if cell.game_object == game_object:
                    return cell.y, cell.x

    def get_cell(self, row: int, col: int) -> Cell:
        """This function is used to get the cell at the given coordinates.

        Args:
            row (int): represents the row of the cell
            col (int): represents the column of the cell

        Returns:
            : Cell: represents the cell at the given coordinates
        """
        return self.cells[row][col]

    def highlight_possible_moves(
        self, pawn: Pawn, selected_card: object
    ) -> list[tuple]:
        """This function is used to highlight the possible moves of a pawn.

        Args:
            pawn (Pawn): represents the pawn
            selected_card (object): represents the selected card and the moves associated

        Returns:
            list[tuple]: represents the possible moves of the pawn
        """
        all_possible_actions = pawn.get_possible_moves(selected_card.moves, self)
        possible_attacks = pawn.get_possible_attacks(selected_card.moves, self)

        # substract the attack positions from the possible moves
        possible_moves = [
            move for move in all_possible_actions if move not in possible_attacks
        ]

        for move_y, move_x in possible_moves:
            cell = self.cells[move_y][move_x]
            cell.highlight()
        for move_y, move_x in possible_attacks:
            cell = self.cells[move_y][move_x]
            cell.highlight((255, 0, 0))

        return all_possible_actions

    def is_valid_move(
        self, clicked_cell_x: int, clicked_cell_y: int, possible_moves: int
    ) -> bool:
        """This function is used to check if the move is valid.

        Args:
            clicked_cell_x (int): cell x coordinate
            clicked_cell_y (int): cell y coordinate
            possible_moves (int): list of possible moves

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return (clicked_cell_x, clicked_cell_y) in possible_moves

    def move_or_attack(
        self, pawn: Pawn, new_y: int, new_x: int, old_coordinates: tuple[int, int]
    ) -> bool:
        """Moves a pawn to a new position.

        Args:
            pawn (Pawn): pawn to move.
            new_x (int): new x coordinate.
            new_y (int): new y coordinate.
            old_coordinates (tuple): old coordinates of the pawn.

        Returns:
            bool: True if the move was successful, False otherwise.
        """

        old_y, old_x = old_coordinates

        # Check if the new cell is occupied
        if self.cells[new_y][new_x].has_enemy():
            # Attack the enemy
            enemy = self.cells[new_y][new_x].game_object

            pawn.attack_target(enemy)
            enemy.take_damage(pawn.attack)
            if enemy.health <= 0:
                self.cells[new_y][new_x].remove_object()
                # REVIEW - Possible drop of loots ?
                return True
            else:
                return False

        # Add the pawn to the new cell

        self.cells[new_y][new_x].add_pawn(pawn)
        # Remove the pawn from the old cell
        self.cells[old_y][old_x].remove_object()
        return True, ""

    def is_empty_or_pawn(self, y: int, x: int):
        """This function is used to check if a cell is occupied.

        Args:
            y (int): y coordinate of a cell
            x (int): x coordinate of a cell

        Returns:
            bool: True if the cell is occupied, False otherwise
        """
        return not (self.cells[y][x].has_pawn() or self.cells[y][x].is_empty)

    def a_star(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """This function is used to find the shortest path between two points.

        Args:
            start (tuple): represents the start point (y, x)
            end (tuple): represents the end point (y, x)

        Returns:
            list[tuple]: represents the shortest path between the two points
        """
        rows, cols = len(self.cells), len(self.cells[0])
        open_list = [start]
        closed_list = set()

        g = {}
        f = {}

        g[start] = 0
        f[start] = self.heuristic(start, end)

        prev = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while open_list:
            # Sort nodes in open list by lowest f score
            current = min(open_list, key=lambda node: f[node])
            open_list.remove(current)
            closed_list.add(current)

            if current == end:
                # Path found, reconstructing
                path = []
                while current in prev:
                    path.append(current)
                    current = prev[current]
                path.append(start)
                # Remove the last node, which is the player's position
                path.pop()
                # Remove the first node, which is the enemy's current position
                path.pop(0)
                return path[::-1]

            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                neighbor = (ny, nx)

                if (
                    0 <= ny < rows
                    and 0 <= nx < cols
                    and self.cells[ny][nx].walkable
                    and not self.is_empty_or_pawn(ny, nx)
                    and neighbor not in closed_list
                ):
                    tentative_g_score = g[current] + 1

                    if neighbor not in open_list:
                        open_list.append(neighbor)
                    elif tentative_g_score >= g[neighbor]:
                        continue

                    # Best path until now, record it
                    prev[neighbor] = current
                    g[neighbor] = tentative_g_score
                    f[neighbor] = g[neighbor] + self.heuristic(neighbor, end)

        # If we reached here, no path was found
        return []

    def heuristic(self, current, goal) -> int:
        """Provides a heuristic for the A* algorithm. Uses Manhattan distance.

        Args:
            current (tuple): current position
            goal (tuple): goal position

        Returns:
            int: heuristic value"""
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def move_enemy(self, enemy: Enemy, player_count: int) -> bool:
        """This function is used to move the enemy.

        Args:
            enemy (Enemy): represents the enemy
            count_player (int): represents the number of players

        Returns:
            bool: True if the enemy was moved, False otherwise
        """
        # FIXME: Implémenter la logique d'IA plus avancée ici.
        ia = enemy.ia
        if ia:
            match player_count:
                case 1:
                    pourcent = 0.6
                case 2:
                    pourcent = 0.7
                case 3:
                    pourcent = 0.85
                case 4:
                    pourcent = 1
            if random.random() >= pourcent:
                ia = False
            else:
                ia = True

        enemy_y, enemy_x = self.get_coordinates_object(enemy)

        self.check_enemy_attack(enemy_x, enemy_y)

        if ia:
            # Find the closest player
            closest_player = None
            closest_distance = float("inf")
            for row in self.cells:
                for cell in row:
                    if cell.game_object and isinstance(cell.game_object, Pawn):
                        distance = math.sqrt(
                            (enemy_y - cell.y) ** 2 + (enemy_x - cell.x) ** 2
                        )
                        if distance < closest_distance:
                            closest_player = cell
                            closest_distance = distance

            # Find the shortest path to the closest player using Dijkstra
            start_node = (enemy_y, enemy_x)
            end_node = (closest_player.y, closest_player.x)
            path = self.a_star(start_node, end_node)
            log.debug("enemy name : %s ; path : %s", enemy.name, path)

            # Move the enemy along the path
            if path:
                next_node = path.pop(0)

                old_y, old_x = enemy_y, enemy_x
                new_y, new_x = next_node[0], next_node[1]
                self.cells[new_y][new_x].add_enemy(enemy)
                self.cells[old_y][old_x].remove_object()
                return True
            else:
                return False

        else:
            while True:
                directions = {
                    "up": lambda y, x: (y - 1, x),
                    "down": lambda y, x: (y + 1, x),
                    "left": lambda y, x: (y, x - 1),
                    "right": lambda y, x: (y, x + 1),
                }
                list_directions = ["up", "down", "left", "right"]
                random.shuffle(list_directions)
                for direction in list_directions:
                    new_y, new_x = directions[direction](enemy_y, enemy_x)
                    if self.cells[new_y][new_x].walkable:
                        if self.cells[new_y][new_x].game_object is None:
                            self.move_or_attack(enemy, new_y, new_x, (enemy_y, enemy_x))
                            return True

    def check_enemy_attack(self, enemy_x: int, enemy_y: int) -> None:
        """This function is used to check if an enemy can attack a pawn."""

        # Get the nearest player
        # TODO - make this a separate function
        closest_player = None
        closest_distance = float("inf")
        for row in self.cells:
            for cell in row:
                if cell.game_object and isinstance(cell.game_object, Pawn):
                    distance = math.sqrt(
                        (enemy_y - cell.y) ** 2 + (enemy_x - cell.x) ** 2
                    )
                    if distance < closest_distance:
                        closest_player = cell
                        closest_distance = distance

        # Check if the enemy can attack the player
        if closest_distance <= 1:
            enemy = self.cells[enemy_y][enemy_x].game_object
            if not enemy.attack_target(closest_player.game_object):
                # The player is dead, remove it from the board
                closest_player.remove_object()

    def draw(
        self, surface: pygame.surface.Surface  # pylint: disable=c-extension-no-member
    ) -> None:
        """This function is used to draw the board and the cells.

        Args:
            surface (pygame.surface.Surface): represents the surface
        """
        for row in self.cells:
            for cell in row:
                cell.draw(surface, self.camera)
                if cell.rect:
                    pygame.draw.rect(
                        surface,
                        (211, 211, 211),
                        (
                            cell.x * GRAPHICAL_TILE_SIZE - self.camera.x,
                            cell.y * GRAPHICAL_TILE_SIZE - self.camera.y,
                            GRAPHICAL_TILE_SIZE,
                            GRAPHICAL_TILE_SIZE,
                        ),
                        1,
                    )

    def tick(self, frame_id: int) -> None:
        """Updates the boards depending on the frame id.

        Args:
            frame_id (int): current frame id
        """
        for row in self.cells:
            for cell in row:
                cell.tick(frame_id)

    def resize_tiles(self, width: int, height: int) -> None:
        """This function is used to resize the tiles.

        Args:
            width (int): represents the width of the tiles
            height (int): represents the height of the tiles
        """
        for row in self.cells:
            for cell in row:
                cell.resize(width, height)

    def _load_from_tmx(
        self,
        tmx_file: str,
        card_map_list: list,
        key_map_list: list,
        rect: bool = False,
    ):
        """This function is used to load the board from a tmx file.

        Args:
            tmx_file (str): represents the tmx file
        """

        tmx_data = pytmx.load_pygame(tmx_file)
        tmx_gids_to_og = tmx_data.tiledgidmap
        og_gids_to_tmx = {v: k for k, v in tmx_data.tiledgidmap.items()}

        self.width = tmx_data.width
        self.height = tmx_data.height
        self.tilewidth = tmx_data.tilewidth
        self.tileheight = tmx_data.tileheight
        self.rect = rect

        # catalogue animated tiles
        props_catalogue = {}
        for gid, props in tmx_data.tile_properties.items():
            props_catalogue[gid] = props

        # log.debug(sorted(props_catalogue.items()))

        # Create cells
        self.cells = [
            [
                Cell(x, y, self.tilewidth, self.tileheight, self.rect)
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

        # layers to draw under the game objects
        layers = []
        layers.append(tmx_data.get_layer_by_name("terrain"))
        layers.append(tmx_data.get_layer_by_name("environment"))
        layers.append(tmx_data.get_layer_by_name("Fake loot"))

        # tmx_data.visible_layers

        for layer in layers:
            if not isinstance(layer, pytmx.TiledTileLayer):
                log.error("Layer %s is not a tile layer", layer.name)
                continue
            for x, y, gid in layer:
                if gid in props_catalogue and props_catalogue[gid]["frames"]:
                    # animated tile
                    frames = []
                    frame_durations = []
                    for frame in props_catalogue[gid]["frames"]:
                        frames.append(tmx_data.get_tile_image_by_gid(frame.gid))
                        frame_durations.append(frame.duration)

                    self.cells[y][x].add_layer(
                        AnimatedTile(
                            props_catalogue[gid].get("walkable", True),
                            frames,
                            frame_durations,
                        )
                    )
                else:
                    # normal tile
                    self.cells[y][x].add_layer(
                        Tile(
                            (
                                props_catalogue[gid].get("walkable", True)
                                if gid in props_catalogue
                                else True
                            ),
                            tmx_data.get_tile_image_by_gid(gid),
                        )
                    )

        # Get all card spawners
        # card_spawns: dict[int : list[tuple[int, int]]] = defaultdict(list)
        # layer = tmx_data.get_layer_by_name("loot")
        # for x, y, tmx_gid in layer:
        #     if tmx_gid != 0:
        #         id_card_spawner = tmx_gid
        #         card_spawns[tmx_gid].append((x, y))

        # # select randomly one of each
        # selected_card_spawns = {}
        # number_of_card_spawns = len(card_spawns[id_card_spawner])
        # print(list_of_cards)
        # print(card_spawns)
        # for tmx_gid in card_spawns:
        #     selected_coordinates = random.sample(
        #         card_spawns[tmx_gid], min(len(list_of_cards), number_of_card_spawns)
        #     )
        #     selected_card_spawns[tmx_gid] = selected_coordinates
        # # add cards to cells
        # # TODO: refactor this
        # unused_cards = list_of_cards.copy()
        # for tmx_gid, coordinates in selected_card_spawns.items():
        #     for coordinate in coordinates:
        #         # get card image based on the original gid
        #         card_random = random.choice(unused_cards)
        #         unused_cards.remove(card_random)
        #         og_gid = tmx_gids_to_og[tmx_gid]
        #         og_gid = og_gid - 10  # valeur en brut en mode balek
        #         img_gid = og_gids_to_tmx[og_gid]

        #         # load animation
        #         frames = []
        #         frame_durations = []
        #         for frame in tmx_data.get_tile_properties_by_gid(img_gid)["frames"]:
        #             frames.append(tmx_data.get_tile_image_by_gid(frame.gid))
        #             frame_durations.append(frame.duration)

        #         card = MapCard(
        #             frames,
        #             frame_durations,
        #             card_random,
        #         )

        #         card.resize(32, 32)
        #         self.cells[coordinate[1]][coordinate[0]].game_object = card

        for row in self.cells:
            for cell in row:
                for card in card_map_list:
                    if card[1] == cell.y and card[2] == cell.x:
                        for default_card in list_of_cards:
                            if card[0] == default_card.name:
                                tmx_gid = card[3]
                                new_card: Card = default_card
                                frames = []
                                frame_durations = []
                                og_gid = tmx_gids_to_og[tmx_gid]
                                og_gid = og_gid - 10  # valeur en brut en mode balek
                                img_gid = og_gids_to_tmx[og_gid]
                                for frame in tmx_data.get_tile_properties_by_gid(
                                    img_gid
                                )["frames"]:
                                    frames.append(
                                        tmx_data.get_tile_image_by_gid(frame.gid)
                                    )
                                    frame_durations.append(frame.duration)
                                new_map_card = MapCard(
                                    frames, frame_durations, new_card
                                )
                                new_map_card.resize(32, 32)
                                cell.game_object = new_map_card

        # resize cells
        for row in self.cells:
            for cell in row:
                cell.resize(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)

        # # Get all key spawners
        # key_spawns: dict[int : list[tuple[int, int]]] = defaultdict(list)
        # layer = tmx_data.get_layer_by_name("keys")
        # for x, y, tmx_gid in layer:
        #     if tmx_gid != 0:
        #         key_spawns[tmx_gid].append((x, y))

        # # select randomly one of each
        # selected_key_spawns = {}
        # for tmx_gid in key_spawns:
        #     selected_key_spawns[tmx_gid] = random.choice(key_spawns[tmx_gid])

        # # add keys to cells
        # list_of_keys_copy = list_of_keys.copy()
        # value = 0
        # for tmx_gid, coordinates in selected_key_spawns.items():
        #     # get key image based on the original gid
        #     og_gid = tmx_gids_to_og[tmx_gid]
        #     og_gid = og_gid - 50  # offset of the sprite sheet (spawner -> key)
        #     img_gid = og_gids_to_tmx[og_gid]

        #     # load animation
        #     frames = []
        #     frame_durations = []
        #     for frame in tmx_data.get_tile_properties_by_gid(img_gid)["frames"]:
        #         frames.append(tmx_data.get_tile_image_by_gid(frame.gid))
        #         frame_durations.append(frame.duration)

        #     key = MapKey(frames, frame_durations, list_of_keys_copy[value])
        #     value += 1

        #     key.resize(32, 32)
        #     self.cells[coordinates[1]][coordinates[0]].game_object = key

        for row in self.cells:
            for cell in row:
                for key in key_map_list:
                    if key[1] == cell.y and key[2] == cell.x:
                        for default_key in list_of_keys:
                            if key[0] == default_key.name:
                                tmx_gid = key[3]
                                new_key: Key = default_key
                                og_gid = tmx_gids_to_og[tmx_gid]
                                og_gid = (
                                    og_gid - 50
                                )  # offset of the sprite sheet (spawner -> key)
                                img_gid = og_gids_to_tmx[og_gid]
                                frames = []
                                frame_durations = []
                                for frame in tmx_data.get_tile_properties_by_gid(
                                    img_gid
                                )["frames"]:
                                    frames.append(
                                        tmx_data.get_tile_image_by_gid(frame.gid)
                                    )
                                    frame_durations.append(frame.duration)
                                new_map_key = MapKey(frames, frame_durations, new_key)
                                new_map_key.resize(32, 32)
                                cell.game_object = new_map_key

        # get the tile props ("heal") for the layer "campfire"
        layer = tmx_data.get_layer_by_name("campfire")
        for x, y, tmx_gid in layer:
            if tmx_gid != 0:
                self.cells[y][x].heal_value = tmx_data.get_tile_properties_by_gid(
                    tmx_gid
                )["heal"]
                self.healing_tiles.append((x, y))

        # resize cells
        for row in self.cells:
            for cell in row:
                cell.resize(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)

    def update_elements(
        self, elements: list[list[str, int, int, int]], possible_moves: list[int, int]
    ) -> None:
        """This function is used to update the elements of the board.

        Args:
            elements (list): represents the elements
        """
        for row in self.cells:
            for cell in row:
                if cell.game_object:
                    found: bool = False
                    for element in elements:
                        if isinstance(cell.game_object, Pawn):
                            if cell.game_object.name == element[0]:
                                pawn = cell.game_object
                                cell.remove_object()
                                pawn.health = element[1]
                                self.cells[element[2]][element[3]].add_pawn(pawn)
                                found = True
                        elif isinstance(cell.game_object, Enemy):
                            if cell.game_object.name == element[0]:
                                enemy = cell.game_object
                                cell.remove_object()
                                enemy.health = element[1]
                                self.cells[element[2]][element[3]].add_enemy(enemy)
                                found = True
                    if not found:
                        if isinstance(cell.game_object, Pawn) or isinstance(
                            cell.game_object, Enemy
                        ):
                            cell.remove_object()

        for row in self.cells:
            for cell in row:
                cell.unhighlight()

        if possible_moves:
            for move_y, move_x in possible_moves:
                cell = self.cells[move_y][move_x]
                cell.highlight()

    # Classmethods

    @classmethod
    def from_tmx(
        cls,
        tmx_file: str,
        camera: tuple[int, int],
        card_map_list: list,
        key_map_list: list,
        rect: bool = False,
    ) -> Board:
        """This function is used to create the board from a tmx file.

        Args:
            tmx_file (str): represents the tmx file
            camera (object): represents the camera
        """

        board = cls(0, 0, 0, 0, camera)
        board._load_from_tmx(
            tmx_file=tmx_file,
            rect=rect,
            card_map_list=card_map_list,
            key_map_list=key_map_list,
        )
        return board
