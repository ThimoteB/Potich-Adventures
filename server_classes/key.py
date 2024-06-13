"""This file contains the key class that will be used to create the keys."""

import logging


log = logging.getLogger(__name__)


class Key:  # pylint: disable=too-few-public-methods
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
        self.name = name


key_slot_width = 80
key_slot_height = 80
list_of_keys = []

red_key = Key("images/red key.png", key_slot_width, key_slot_height, "red key")
blue_key = Key("images/blue key.png", key_slot_width, key_slot_height, "blue key")
green_key = Key("images/green key.png", key_slot_width, key_slot_height, "green key")
yellow_key = Key("images/yellow key.png", key_slot_width, key_slot_height, "yellow key")
list_of_keys.append(blue_key)
list_of_keys.append(green_key)
list_of_keys.append(red_key)
list_of_keys.append(yellow_key)
