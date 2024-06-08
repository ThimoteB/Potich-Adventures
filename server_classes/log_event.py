""" This module is used to create the log_event."""
import pygame


class LogEvent(pygame.sprite.Sprite):
    """This class is used to create the game info."""

    def __init__(self, 
                #  screen, 
                 width: int, 
                 height: int, 
                 space_from_top: int):
        """This function is used to initialize the log event.

        Args:
            -screen (pygame.surface): represents the screen-
            width (int): represents the width of the game info
            height (int): represents the height of the game info
        """
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.list_log = [""]
        # self.base_text_rect = (screen.get_width() - width - 40, space_from_top)
        # self.base_y = screen.get_height()
        self.space_from_top = space_from_top
        self.width = width
        self.height = height
        self.count_reset = 1
        self.reset = False
        self.reset_logfile("log_event.txt")

    def read_logfile(self, log_file: str):
        with open(log_file, "r") as file:
            lines = file.readlines()

            if lines:
                try:
                    self.count_reset = int(lines[0].rstrip("\n"))
                except ValueError:
                    self.count_reset = 0

            self.list_log = [line.rstrip("\n") for line in lines[1:]]

    def write_logfile(self, log_file: str, text: str):
        with open(log_file, "r+") as file:
            lines = file.readlines()

            if lines:
                try:
                    first_line_number = int(lines[0].strip()) + 1
                    lines[0] = f"{first_line_number}\n"
                except ValueError:
                    pass

            text_written = False
            for i in range(1, len(lines)):
                if not lines[i].strip():
                    lines[i] = text + "\n"
                    text_written = True
                    break

            if not text_written:
                lines.append(text + "\n")

            file.seek(0)
            file.writelines(lines)

    def reset_logfile(self, log_file: str):
        """This function is used to reset the log file.

        Args:
            log_file (str): represents the path of the log file
        """
        with open(log_file, "w") as file:
            file.write("0")

    # def draw_text(self, screen: pygame.surface):
    #     """This function is used to draw the game info.

    #     Args:
    #         screen (pygame.surface): represents the screen
    #     """
    #     self.list_log = [""]
    #     self.read_logfile("log_event.txt")

    #     while len(self.list_log) > 5:
    #         self.list_log.pop(0)

    #     # print(f"Liste a afficher : {self.list_log}")
    #     for i, log in enumerate(self.list_log):
    #         text = self.font.render(log, True, (self.color))
    #         text_rect = text.get_rect()
    #         text_rect.topleft = (
    #             self.base_text_rect[0],
    #             self.base_text_rect[1] + i * text_rect.height,
    #         )
    #         screen.blit(text, text_rect)

    #     # print(text_rect.y)
    #     # if text_rect.y > self.space_from_top + self.height:
    #     #     self.list_log.pop(0)
