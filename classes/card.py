"""This file contains the card class that will be used to create the cards."""

import logging

import pygame

from moves import (
    move_croix,
    move_down_1,
    move_down_2,
    move_fontaine,
    move_horloge,
    move_left_1,
    move_left_2,
    move_lightning,
    move_plume,
    move_right_1,
    move_right_2,
    move_supreme,
    move_up_1,
    move_up_2,
)

from game_constants.consts import CARD_SLOT_HEIGHT, CARD_SLOT_WIDTH

log = logging.getLogger(__name__)


class Card(pygame.sprite.Sprite):  # pylint: disable=too-few-public-methods
    """This class is used to create the cards.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(
        self,
        image_path: str,
        width: int,
        height: int,
        moves: list = None,
        name: str = None,
    ):
        """This function is used to initialize the card.

        Args:
            image_path (str): represents the path of the image
            width (int): represents the width of the card
            height (int): represents the height of the card
            moves (list, optional): represents the moves of the card. Defaults to None.
        """
        super().__init__()
        self.image = pygame.image.load(image_path)  # Load the image
        if self.image:
            self.image = pygame.transform.scale(
                self.image, (width, height)
            )  # Resize the image
            self.rect = self.image.get_rect()
        else:
            log.error("Failed to load image from path: %s", image_path)
        self.selected = False
        self.moves = moves
        self.name = name

    def toggle_select(self):
        """This function is used to select the card."""
        self.selected = not self.selected
        log.debug("Selected: %s", self.selected)
        # log.debug("Moves: %s", self.moves) # crashes the game if the "SUPREME CARD" is selected

    @property
    def get_name(self):
        """Returns the name of the card."""
        # TODO: refactor self.name to self._name and change the "get_name" property to "name"
        return self.name


list_of_cards = []
card_croix = Card(
    "images/croix.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_croix, "Croix"
)
card_lightning = Card(
    "images/lightning.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_lightning, "Eclair"
)
card_horloge = Card(
    "images/horloge.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_horloge, "Horloge"
)
card_fontaine = Card(
    "images/fontaine.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_fontaine, "Fontaine"
)
card_plume = Card(
    "images/plume.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_plume, "Plume"
)
card_up_1 = Card("images/up_1.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_up_1, "Up1")
card_up_2 = Card("images/up_2.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_up_2, "Up2")
card_down_1 = Card(
    "images/down_1.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_down_1, "Down1"
)
card_down_2 = Card(
    "images/down_2.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_down_2, "Down2"
)
card_left_1 = Card(
    "images/left_1.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_left_1, "Left1"
)
card_left_2 = Card(
    "images/left_2.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_left_2, "Left2"
)
card_right_1 = Card(
    "images/right_1.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_right_1, "Right1"
)
card_right_2 = Card(
    "images/right_2.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_right_2, "Right2"
)
card_supreme = Card(
    "images/supreme.png", CARD_SLOT_WIDTH, CARD_SLOT_HEIGHT, move_supreme, "Supreme"
)

list_of_cards.append(card_croix)
list_of_cards.append(card_lightning)
list_of_cards.append(card_horloge)
list_of_cards.append(card_fontaine)
list_of_cards.append(card_plume)
# list_of_cards.append(card_up_1)
list_of_cards.append(card_up_2)
# list_of_cards.append(card_down_1)
list_of_cards.append(card_down_2)
# list_of_cards.append(card_left_1)
list_of_cards.append(card_left_2)
# list_of_cards.append(card_right_1)
list_of_cards.append(card_right_2)
