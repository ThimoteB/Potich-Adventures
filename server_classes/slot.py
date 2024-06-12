""" This module is used to create the slots for the cards and the keys."""
import pygame


class Slot:
    """This class is used to create slots for cards or keys.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(
        # self, screen: pygame.surface, width: int, height: int, position: tuple
        self
    ):
        """This function is used to initialize the slots
        that will just be used to store cards or keys.

        Args:
            screen (pygame.surface): represents the screen
            width (int): represents the width of the slot
            height (int): represents the height of the slot
            position (tuple): represents the position of the slot
        """
        super().__init__()
        # self.image = pygame.Surface((width, height))
        # self.rect = self.image.get_rect()
        # self.rect.topleft = position
        # self.color = (255, 255, 255)
        # self.image.fill(self.color)
        self.item = None
        # self.screen = screen

    # def draw(self):
    #     """This function is used to draw the slots."""
    #     self.screen.blit(self.image, self.rect)

    def is_empty(self):
        """This function is used to check if the slot is empty.

        Returns:
            bool : True if the slot is empty, False otherwise
        """
        return self.item is None

    def add_item(self, item):
        """This function is used to add an item (card or key) to the slot.

        Args:
            item (object): represents the item that will be added to the slot
        """
        if self.is_empty():
            self.item = item

    def reset_item(self):
        """This function is used to reset the item in the slot."""
        self.item = None


class CardSlot(Slot):
    """This class is used to create the card slots.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(  # pylint: disable=useless-super-delegation
        self,
        # screen: pygame.surface,
        # width: int,
        # height: int,
        # position: tuple,
        # image: str,
    ):
        # super().__init__(screen, width, height, position)
        # self.image = pygame.image.load(image)
        # self.image = pygame.transform.scale(self.image, (150, 220))
        pass


class KeySlot(Slot):
    """This class is used to create the key slots.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(  # pylint: disable=useless-super-delegation
        self
    ):
        # super().__init__(screen, width, height, position)
        super().__init__()
        pass
