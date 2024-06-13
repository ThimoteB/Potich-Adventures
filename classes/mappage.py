""" This file contains the map page class that will be used to create the map page."""

import random
import pygame


class MapPage:
    """This class is used to create the map page."""

    def __init__(self, screen: pygame.display):  # pylint: disable=redefined-outer-name
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.image = pygame.image.load("images/map1.png")  # Chargez l'image de la carte
        self.image = pygame.transform.scale(
            self.image, (500, 500)
        )  # Redimensionnez l'image à 500x500
        self.map_name = "Pingouin Etrange"  # Nom de la carte
        self.selected_map_index = 0  # Indice de la carte actuellement sélectionnée
        self.map_names = {
            "Pingouin Etrange": "map1.tmx",
            "Pomme usagé": "map2.tmx",
            "Capitaine Crabe": "map3.tmx",
            "Cimetière enneigé....": "map4.tmx",
            "Niceee Luck": "map5.tmx",
            "Demo": "map_courte.tmx",
        }
        self.map_path = {
            "Pingouin Etrange": "images/map1.png",
            "Pomme usagé": "images/map2.png",
            "Capitaine Crabe": "images/map3.png",
            "Cimetière enneigé....": "images/map4.png",
            "Niceee Luck": "images/map5.png",
            "Demo": "images/map_courte.png",
        }
        self.button_text = "Start the game"  # Texte du bouton
        self.button_rect = pygame.Rect(100, 400, 200, 50)  # Rectangle du bouton
        self.hitbox_start = None
        self.hitbox_fog = None
        self.hitbox_random = None
        self.left_arrow = None
        self.right_arrow = None
        self.fog = False

        self.map_chosen = "map1.tmx"

    def draw(self):
        """This function is used to draw the map page."""
        self.screen.fill((0, 0, 0))  # Fond noir

        # Obtenez les dimensions de l'image
        image_width, image_height = self.image.get_size()

        # Calculez les coordonnées pour centrer l'image dans la fenêtre
        x = (self.screen.get_width() - image_width) // 2
        y = (self.screen.get_height() - image_height) // 2

        # Afficher l'image de la carte centrée
        self.screen.blit(self.image, (x, y))

        self.left_arrow = pygame.draw.polygon(
            self.screen,
            (255, 255, 255),
            [
                (x - 75, y + image_height // 2),
                (x - 55, y + image_height // 2 - 20),
                (x - 55, y + image_height // 2 + 20),
            ],
        )
        self.right_arrow = pygame.draw.polygon(
            self.screen,
            (255, 255, 255),
            [
                (x + image_width + 75, y + image_height // 2),
                (x + image_width + 55, y + image_height // 2 - 20),
                (x + image_width + 55, y + image_height // 2 + 20),
            ],
        )

        # Afficher le nom de la carte en dessous de l'image
        text_map = self.font.render(self.map_name, True, (255, 255, 255))
        text_rect_map = text_map.get_rect(
            center=(self.screen.get_width() // 2, y + image_height + 20)
        )
        self.screen.blit(text_map, text_rect_map)

        # Afficher le bouton "Start the game" en dessous du nom
        text_start = self.font.render(self.button_text, True, (255, 255, 255))
        text_rect_start = text_start.get_rect(
            center=(self.screen.get_width() // 2, y + image_height + 170)
        )
        self.hitbox_start = text_rect_start.inflate(10, 10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.hitbox_start, 2)

        # FOG

        text_fog = self.font.render("Fog", True, (255, 255, 255))
        text_rect_fog = text_fog.get_rect(
            center=(self.screen.get_width() // 2, y + image_height + 70)
        )
        self.hitbox_fog = text_rect_fog.inflate(10, 10)

        # RANDOM
        text_random = self.font.render("Random", True, (255, 255, 255))
        text_rect_random = text_random.get_rect(
            center=(self.screen.get_width() // 2, y + image_height + 120)
        )
        self.hitbox_random = text_rect_random.inflate(10, 10)

        if not self.fog:
            pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox_fog, 2)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), self.hitbox_fog, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), self.hitbox_random, 2)
        self.screen.blit(text_start, text_rect_start)
        self.screen.blit(text_fog, text_rect_fog)
        self.screen.blit(text_random, text_rect_random)

    def update_selected_map(self, index: int):
        """This function is used to update the selected map.

        Args:
            index (int): represents the index of the map
        """
        map_items_list = list(self.map_names.items())
        self.selected_map_index = index
        self.map_name, self.map_chosen = map_items_list[index]
        self.image = pygame.image.load(self.map_path[self.map_name])
        self.image = pygame.transform.scale(self.image, (500, 500))

    def on_click(self, mouse_pos: tuple) -> bool:
        """This function is used to check if the map page is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse

        Returns:
            bool : True if an arrow is clicked, False otherwise
        """
        if self.hitbox_start.collidepoint(mouse_pos):
            return True

        if self.left_arrow.collidepoint(pygame.mouse.get_pos()):
            self.selected_map_index -= 1
            if self.selected_map_index < 0:
                self.selected_map_index = len(self.map_names) - 1
            self.update_selected_map(self.selected_map_index)

        if self.right_arrow.collidepoint(pygame.mouse.get_pos()):
            self.selected_map_index += 1
            if self.selected_map_index >= len(self.map_names):
                self.selected_map_index = 0
            self.update_selected_map(self.selected_map_index)

    def return_map(self):
        """This function is used to return the map chosen."""
        return self.map_chosen

    def return_fog(self):
        """This function is used to return the fog."""
        return self.fog

    def on_click_fog(self, mouse_pos: tuple) -> bool:
        """This function is used to check if the map page is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse

        Returns:
            bool : True if an arrow is clicked, False otherwises
        """
        if self.hitbox_fog.collidepoint(mouse_pos):
            return True

    def handle_fog(self):
        """This function is used to handle the fog."""
        if self.fog:
            self.fog = False
        else:
            self.fog = True

    def on_click_random(self, mouse_pos: tuple) -> bool:
        """This function is used to check if the map page is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse

        Returns:
            bool : True if an arrow is clicked, False otherwise
        """
        if self.hitbox_random.collidepoint(mouse_pos):
            return True

    def handle_random(self):
        """This function is used to handle the random."""
        map_items_list = list(self.map_names.items())
        random_map = random.choice(map_items_list)
        self.map_name, self.map_chosen = random_map
        self.fog = random.choice([True, False])
        return self.map_chosen, self.fog


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(
        flags=pygame.FULLSCREEN  # pylint: disable=no-member
    )
    map_page = MapPage(screen)

    while True:
        map_page.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if map_page.on_click_fog(pygame.mouse.get_pos()):
                    map_page.handle_fog()
                map_page.on_click(pygame.mouse.get_pos())

        pygame.display.flip()
