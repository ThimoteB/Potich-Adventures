"""This file contains the key class that will be used to create the keys."""

import logging

import pygame

from game_constants.consts import KEY_SLOT_HEIGHT, KEY_SLOT_WIDTH

log = logging.getLogger(__name__)


class Key(pygame.sprite.Sprite):  # pylint: disable=too-few-public-methods
    """This class is used to create the keys IN THE SIDEBAR.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(self, image_path: str, width: int, height: int, name: str):
        """This function is used to initialize the keys.

        Args:
            image_path (str): represents the path of the image
            width (int): represents the width of the key
            height (int): represents the height of the key
        """
        super().__init__()
        self.image = pygame.image.load(image_path)  # Load the image
        self.name = name
        if self.image:
            self.image = pygame.transform.scale(
                self.image, (width, height)
            )  # Resize the image
            self.rect = self.image.get_rect()
        else:
            log.error("Failed to load image from path: %s", image_path)


list_of_keys: list[Key] = []

red_key = Key("images/red key.png", KEY_SLOT_WIDTH, KEY_SLOT_HEIGHT, "red key")
blue_key = Key("images/blue key.png", KEY_SLOT_WIDTH, KEY_SLOT_HEIGHT, "blue key")
green_key = Key("images/green key.png", KEY_SLOT_WIDTH, KEY_SLOT_HEIGHT, "green key")
yellow_key = Key("images/yellow key.png", KEY_SLOT_WIDTH, KEY_SLOT_HEIGHT, "yellow key")
list_of_keys.append(blue_key)
list_of_keys.append(green_key)
list_of_keys.append(red_key)
list_of_keys.append(yellow_key)
