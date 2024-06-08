""" This file contains the map page class that will be used to create the map page."""
import pygame


class RulePage:
    """This class is used to create the map page."""

    def __init__(self, screen: pygame.display):  # pylint: disable=redefined-outer-name
        self.screen = screen
        self.image_index = 0  # Indice de la carte actuellement sélectionnée
        self.images = [
            "images/tuto_1.png",
            "images/tuto_2.png",
            "images/tuto_3.png",
            "images/tuto_4.png",
            "images/tuto_5.png",
            "images/tuto_6.png",
            "images/tuto_7.png",
            "images/tuto_8.png",
            "images/tuto_9.png",
            "images/tuto_10.png",
        ]

        self.left_arrow = None
        self.right_arrow = None

        self.left_arrow_color = (100, 100, 100)
        self.right_arrow_color = (255, 255, 255)

        self.image = pygame.image.load(self.images[0])

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
            self.left_arrow_color,
            [
                (x - 75, y + image_height // 2),
                (x - 55, y + image_height // 2 - 20),
                (x - 55, y + image_height // 2 + 20),
            ],
        )
        self.right_arrow = pygame.draw.polygon(
            self.screen,
            self.right_arrow_color,
            [
                (x + image_width + 75, y + image_height // 2),
                (x + image_width + 55, y + image_height // 2 - 20),
                (x + image_width + 55, y + image_height // 2 + 20),
            ],
        )

    def update_image(self):
        """This function is used to change the image of the map page.

        Args:
            image_index (int): represents the index of the image to be displayed
        """
        self.image = pygame.image.load(self.images[self.image_index])

    def on_click(self, mouse_pos: tuple) -> bool:
        """This function is used to check if the map page is clicked.

        Args:
            mouse_pos (tuple): represents the position of the mouse

        Returns:
            bool : True if an arrow is clicked, False otherwise
        """

        if self.left_arrow.collidepoint(mouse_pos):
            self.image_index -= 1
            if self.image_index <= 0:
                self.image_index = 0
                self.left_arrow_color = (100, 100, 100)
            self.right_arrow_color = (255, 255, 255)
            self.update_image()

        if self.right_arrow.collidepoint(mouse_pos):
            self.image_index += 1
            if self.image_index >= len(self.images) - 1:
                self.image_index = len(self.images) - 1
                self.right_arrow_color = (100, 100, 100)
            self.left_arrow_color = (255, 255, 255)
            self.update_image()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(
        flags=pygame.FULLSCREEN  # pylint: disable=no-member
    )
    map_page = RulePage(screen)

    while True:
        map_page.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                map_page.on_click(pygame.mouse.get_pos())

        pygame.display.flip()
