""" This module contains the Pawn class and its subclasses."""
import logging

import pygame

from game_constants.consts import GRAPHICAL_TILE_SIZE
from .entity import Entity
from .enemy import Enemy

log = logging.getLogger(__name__)


class Pawn(Entity):
    """This class is used to create the pawns.
    We will use her subclasses to create the different types of pawns.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(
        self,
        # image: pygame.Surface,
        name: str,
        health: int,
        attack: int,
        element="Neutral",
    ):
        super().__init__(# image, 
                         name, 
                         health, 
                         attack, 
                         element)
        # self.resize(GRAPHICAL_TILE_SIZE, GRAPHICAL_TILE_SIZE)

    def _transform_move(self, move):
        """Transforms the move matrix from X Y format to Y X format."""
        return [[move[j][i] for j in range(len(move))] for i in range(len(move[0]))]

    def get_possible_moves(self, move, board) -> list[tuple[int, int]]:
        """Returns a list of possible moves for the pawn.

        Args:
            move (list[list[int]]): The move matrix.
            board (Board): The board instance.

        Returns:
            list[tuple[int, int]]: A list of possible moves for the pawn.
        """
        move = self._transform_move(move)
        get_possible_moves_coords = []
        col, row = board.get_coordinates_object(self)
        log.debug("POSITIONS DU PION : %s, %s", col, row)

        current_row, current_col = None, None
        # pylint: disable=consider-using-enumerate
        for r in range(len(move)):
            for c in range(len(move[r])):
                if move[r][c] == 2:
                    current_row, current_col = r, c
                    break
                if (
                    current_row is not None
                ):  # break out of the outer loop if current_row is found
                    break

        if current_row is not None and current_col is not None:
            for r in range(len(move)):
                for c in range(len(move[r])):
                    if move[r][c] > 0 and move[r][c] != 2:
                        new_col = col + c - current_col
                        new_row = row + r - current_row
                        if 0 <= new_row < 100 and 0 <= new_col < 100:
                            # Si la case est walkable,on l'ajoute à la liste des positions possibles
                            if board.get_cell(new_col, new_row).walkable:
                                if not isinstance(
                                    board.get_cell(new_col, new_row).game_object, Pawn
                                ):
                                    get_possible_moves_coords.append((new_col, new_row))

        return get_possible_moves_coords

    def get_possible_attacks(self, move, board) -> list[tuple[int, int]]:
        """Same as get_possible_moves, but instead select only tiles that contain the "Enemy" class."""

        move = self._transform_move(move)
        get_possible_moves_coords = []
        col, row = board.get_coordinates_object(self)
        log.debug(f"POSITIONS DU PION : {col}, {row}")

        current_row, current_col = None, None
        # pylint: disable=consider-using-enumerate
        for r in range(len(move)):
            for c in range(len(move[r])):
                if move[r][c] == 2:
                    current_row, current_col = r, c
                    break
                if (
                    current_row is not None
                ):  # break out of the outer loop if current_row is found
                    break

        if current_row is not None and current_col is not None:
            for r in range(len(move)):
                for c in range(len(move[r])):
                    if move[r][c] > 0 and move[r][c] != 2:
                        new_col = col + c - current_col
                        new_row = row + r - current_row
                        if 0 <= new_row < 100 and 0 <= new_col < 100:
                            if board.get_cell(new_col, new_row).walkable:
                                if isinstance(
                                    board.get_cell(new_col, new_row).game_object, Enemy
                                ):
                                    get_possible_moves_coords.append((new_col, new_row))

        return get_possible_moves_coords