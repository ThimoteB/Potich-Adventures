""" This file contains the tab class that will be used to create the tab. """
import pygame  # pylint: disable=import-error
from .greyzone import GreyZone  # pylint: disable=no-name-in-module
from .blackzone import BlackZone  # pylint: disable=no-name-in-module
from .gameinfo import GameInfo  # pylint: disable=no-name-in-module
from .slot import CardSlot, KeySlot  # pylint: disable=no-name-in-module
from .log_event import LogEvent  # pylint: disable=no-name-in-module


class Tab(pygame.sprite.Sprite):
    """This class is used to create the tab.

    Args:
        pygame (_type_): Sprite class from pygame
    """

    def __init__(
        self,
        # screen: pygame.surface,
        # width: int,
        # height: int,
        # gray_width: int,
        # black_width: int = 500,
    ):
        """This function is used to initialize the tab.

        Args:
            screen (pygame.surface): represents the screen
            width (int): represents the width of the tab
            height (int): represents the height of the tab
            gray_width (int): represents the width of the grey zone
            black_width (int, optional): represents the width of the black zone. Defaults to 500.
        """
        # self.screen = screen
        # self.width = width
        # self.height = height
        # self.gray_width = gray_width
        # self.black_width = black_width
        # self.gray_zone = GreyZone(screen, gray_width, height)
        # self.black_zone = BlackZone(screen, black_width, height, gray_width)
        # self.is_expanded = False
        self.card_group = []
        self.key_group = []

        # Width and height of the slots
        # self.card_slot_width = 150
        # self.card_slot_height = 220
        # self.key_slot_width = 80
        # self.key_slot_height = 80
        # self.key_slot_height_from_top = 150
        # self.log_event_height = 200
        # self.log_event_width = 480
        # self.log_event_from_tom = 300

        # space_between_slots_cards = (black_width - 2 * self.card_slot_width) / 3
        # space_between_slots_keys = (black_width - 4 * self.key_slot_width) / 5
        # card_slot_y_bottom = self.screen.get_height() - (50 + self.card_slot_height)
        # card_sloy_y_top = self.screen.get_height() - 2 * (50 + self.card_slot_height)
        # base_x = self.screen.get_width() - gray_width - black_width

        ### LOG EVENT
        # self.log_event = LogEvent(
        #     self.log_event_width, self.log_event_height, self.log_event_from_tom
        # )
        ### GAME INFO

        # self.game_info = GameInfo(screen, black_width, gray_width, 100)
        ### CARD SLOT
        # Calcul of the different slots positions

        # first_bottom_slots_y = card_slot_y_bottom
        # first_bottom_slot_x = base_x + space_between_slots_cards

        # second_bottom_slots_y = card_slot_y_bottom
        # second_bottom_slot_x = (
        #     base_x + self.card_slot_width + 2 * space_between_slots_cards
        # )

        # first_top_slots_y = card_sloy_y_top
        # first_top_slot_x = base_x + space_between_slots_cards

        # second_top_slots_y = card_sloy_y_top
        # second_top_slot_x = (
        #     base_x + self.card_slot_width + 2 * space_between_slots_cards
        # )

        # Creation of the slots
        self.bottom_left_slot = CardSlot(
            # self.screen,
            # self.card_slot_width,
            # self.card_slot_height,
            # (first_bottom_slot_x, first_bottom_slots_y),
            # "images/carte.jpg",
        )

        self.bottom_right_slot = CardSlot(
            # self.screen,
            # self.card_slot_width,
            # self.card_slot_height,
            # (second_bottom_slot_x, second_bottom_slots_y),
            # "images/carte.jpg",
        )

        self.top_left_slot = CardSlot(
            # self.screen,
            # self.card_slot_width,
            # self.card_slot_height,
            # (first_top_slot_x, first_top_slots_y),
            # "images/carte.jpg",
        )

        self.top_right_slot = CardSlot(
            # self.screen,
            # self.card_slot_width,
            # self.card_slot_height,
            # (second_top_slot_x, second_top_slots_y),
            # "images/carte.jpg",
        )

        # Add the slots to the card group
        # self.card_group.add(
        #     self.top_left_slot,
        #     self.top_right_slot,
        #     self.bottom_left_slot,
        #     self.bottom_right_slot,
        # )
        
        self.card_group.append(self.top_left_slot)
        self.card_group.append(self.top_right_slot)
        self.card_group.append(self.bottom_left_slot)
        self.card_group.append(self.bottom_right_slot)
        

        ### KEY SLOT

        # first_key_slot_x = base_x + space_between_slots_keys
        # first_top_slots_y = self.key_slot_height_from_top

        # second_key_slot_x = base_x + self.key_slot_width + 2 * space_between_slots_keys
        # second_top_slots_y = self.key_slot_height_from_top

        # third_key_slot_x = (
        #     base_x + 2 * self.key_slot_width + 3 * space_between_slots_keys
        # )
        # third_top_slots_y = self.key_slot_height_from_top

        # fourth_key_slot_x = (
        #     base_x + 3 * self.key_slot_width + 4 * space_between_slots_keys
        # )
        # fourth_top_slots_y = self.key_slot_height_from_top

        self.first_key_slot = KeySlot(
            # self.screen,
            # self.key_slot_width,
            # self.key_slot_height,
            # (first_key_slot_x, first_top_slots_y),
        )

        self.second_key_slot = KeySlot(
            # self.screen,
            # self.key_slot_width,
            # self.key_slot_height,
            # (second_key_slot_x, second_top_slots_y),
        )

        self.third_key_slot = KeySlot(
            # self.screen,
            # self.key_slot_width,
            # self.key_slot_height,
            # (third_key_slot_x, third_top_slots_y),
        )

        self.fourth_key_slot = KeySlot(
            # self.screen,
            # self.key_slot_width,
            # self.key_slot_height,
            # (fourth_key_slot_x, fourth_top_slots_y),
        )

        # self.key_group.add(
        #     self.first_key_slot,
        #     self.second_key_slot,
        #     self.third_key_slot,
        #     self.fourth_key_slot,
        # )
        
        self.key_group.append(self.first_key_slot)
        self.key_group.append(self.second_key_slot)
        self.key_group.append(self.third_key_slot)
        self.key_group.append(self.fourth_key_slot)
        

    # def draw_cards(self, screen: pygame.surface):
    #     """This function is used to draw the cards on their slots.

    #     Args:
    #         screen (pygame.surface): represents the screen
    #     """
    #     for slot in self.card_group:
    #         if not slot.is_empty():
    #             card = slot.item
    #             # Draw the card on the slot
    #             card.rect.topleft = slot.rect.topleft
    #             screen.blit(card.image, card.rect)
    #             if card.selected:  # Verify if the card is selected
    #                 pygame.draw.rect(
    #                     screen, (0, 255, 0), card.rect, 2
    #                 )  # # Draw a green rectangle around the selected card
    #             else:
    #                 pygame.draw.rect(
    #                     screen, (255, 0, 0), card.rect, 2
    #                 )  # Draw a red rectangle around the unselected card

    # def draw_keys(self, screen: pygame.surface):
    #     """This function is used to draw the keys on their slots.

    #     Args:
    #         screen (pygame.surface): represents the screen
    #     """
    #     for slot in self.key_group:
    #         if not slot.is_empty():
    #             key = slot.item
    #             # Draw the key on the slot
    #             key.rect.topleft = slot.rect.topleft
    #             screen.blit(key.image, key.rect)

    def is_card_selected(self, card):
        """This function is used to know if a card is selected.

        Args:
            card (Card): represents the card

        Returns:
            bool: True if the card is selected, False otherwise
        """
        return card.selected

    def unselect_all_cards(self):
        """This function is used to unselect all the cards."""
        for card_slot in self.card_group:
            if card_slot.item and card_slot.item.selected:
                card_slot.item.toggle_select()

    # def toggle_expand(self):
    #     """This function is used to expand the tab."""
    #     self.is_expanded = not self.is_expanded
    #     self.black_zone.visible = self.is_expanded

    # def draw(self, screen: pygame.surface):
    #     """This function is used to draw the tab.

    #     Args:
    #         screen (pygame.surface): represents the screen
    #     """
    #     if self.is_expanded:
    #         self.gray_zone.draw(screen)
    #         if self.black_zone.visible:
    #             self.black_zone.draw(screen)
    #         self.card_group.draw(screen)  # Draw the card slots
    #         self.draw_cards(screen)  # Draw the cards on their slots
    #         self.key_group.draw(screen)
    #         self.draw_keys(screen)
    #         self.game_info.draw_gameinfo(screen)
    #         self.log_event.draw_text(screen)
    #     else:
    #         self.gray_zone.draw(screen)

    def handle_input(self, mouse_pos: tuple):
        """This function is used to detect if the grey zone is clicked for expanding the tab.

        Args:
            mouse_pos (tuple): represents the position of the mouse
        """
        if (
            mouse_pos[0] >= self.gray_zone.rect.left
            and mouse_pos[0] <= self.gray_zone.rect.right
            and mouse_pos[1] >= self.gray_zone.rect.top
            and mouse_pos[1] <= self.gray_zone.rect.bottom
        ):
            self.toggle_expand()

    def handle_click(self, mouse_pos: tuple):
        """This function is used to detect if a card is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse
        """
        if self.is_expanded:
            for card_slot in self.card_group:
                if card_slot.item and card_slot.item.rect.collidepoint(mouse_pos):
                    clicked_card = card_slot.item
                    if clicked_card.selected:
                        # If the clicked card is already selected, unselect it
                        clicked_card.toggle_select()
                        return clicked_card  # Set card_selected to None
                    else:
                        # Unselect all the other cards
                        for other_card_slot in self.card_group:
                            if other_card_slot.item != clicked_card:
                                other_card = other_card_slot.item
                                if other_card and other_card.selected:
                                    other_card.toggle_select()
                        clicked_card.toggle_select()
                        return clicked_card

    def handle_click_shortcut_cards(self, index: int):
        """This function is used to detect if a card is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse
        """
        card_slot = self.card_group.sprites()[index]
        clicked_card = card_slot.item
        if clicked_card != None:
            if clicked_card.selected:
                # If the clicked card is already selected, unselect it
                clicked_card.toggle_select()
                return clicked_card  # Set card_selected to None
            else:
                # Unselect all the other cards
                for other_card_slot in self.card_group:
                    if other_card_slot.item != clicked_card:
                        other_card = other_card_slot.item
                        if other_card and other_card.selected:
                            other_card.toggle_select()
                clicked_card.toggle_select()
                return clicked_card
        else:
            self.unselect_all_cards()

    def shortcut_cards(self, index: int, number_of_cards: int):
        """This function is used to select a card with a shortcut.

        Args:
            index (int): represents the index of the card in the card group
            number_of_cards (int): represents the number of cards in the card group

        Returns:
            Card: the card selected
        """
        """
        elif pygame.key.get_pressed()[pygame.K_4]:
                    if len(self.queue.queue[0].cards) >= 4:
                        card_selected = self.queue.queue[0].cards[3]
                        self.unhilight()
                        highlighted_cells = []
                        self.tab.unselect_all_cards()
                        self.tab.bottom_right_slot.item.toggle_select()
                        self.tab.draw_cards(self.screen)
                        pygame.display.flip()
        """
        match index:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                if number_of_cards >= 4:
                    card_slot = self.card_group.sprites()[3]
                    card_selected = card_slot.item
                    if card_selected.selected:
                        # If the clicked card is already selected, unselect it
                        card_selected.toggle_select()
                        return card_selected  # Set card_selected to None
                    else:
                        # Unselect all the other cards
                        for other_card_slot in self.card_group:
                            if other_card_slot.item != card_selected:
                                other_card = other_card_slot.item
                                if other_card and other_card.selected:
                                    other_card.toggle_select()
                        card_selected.toggle_select()
