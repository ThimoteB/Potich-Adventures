"""Entity base class."""

from __future__ import annotations
import logging

import pygame

from game_constants.consts import GRAPHICAL_TILE_SIZE, SOUND
from .object_bases import ObjectBase

log = logging.getLogger(__name__)


class Entity(ObjectBase):
    """Base class for all entities (pawns, enemies, etc.)."""

    ELEMENT_ADVANTAGES = {
        "Fire": {"Fire": 0, "Water": -1, "Grass": 1, "Neutral": 0},
        "Water": {"Fire": 1, "Water": 0, "Grass": -1, "Neutral": 0},
        "Grass": {"Fire": -1, "Water": 1, "Grass": 0, "Neutral": 0},
        "Neutral": {"Fire": 0, "Water": 0, "Grass": 0, "Neutral": 0},
    }

    def __init__(
        self,
        image: pygame.Surface,
        name: str,
        health: int,
        attack: int,
        element: str,
        draw_healthbar: bool = True,
    ):
        super().__init__(image)
        self.name = name
        self.health = health
        self.attack = attack
        self.element = element

        self.rect = self._image.get_rect()

        self.draw_healthbar = draw_healthbar
        self.max_health = health
        self.healthbar = pygame.Surface((GRAPHICAL_TILE_SIZE, 5))

    def take_damage(self, damage: int) -> bool:
        """This method is used to take damage.

        Args:
            damage (int): The amount of damage to take.
        Returns:
            bool: True if the entity is still alive, False otherwise.
        """
        self.health -= damage
        if SOUND:
            damage_sound = pygame.mixer.Sound("sounds/damage.mp3")
            damage_sound.play()
        if self.health <= 0:
            log.info("%s has been defeated!", self.name)
            self.write_logfile("log_event.txt", f"{self.name} nous a quitté :(")
            if SOUND:
                death_sound = pygame.mixer.Sound("sounds/Death.mp3")
                death_sound.play()
            return False
        return True

    def attack_target(self, target: Entity) -> bool:
        """This method is used to attack a target.

        Args:
            target (Entity): The target to attack.
        Returns:
            bool: True if the target is still alive, False otherwise.
        """
        log.info(f"{self.name} attacks {target.name}!")

        total_damage = max(
            self.ELEMENT_ADVANTAGES[self.element][target.element] + self.attack, 0
        )
        self.write_logfile("log_event.txt", f"{self.name} a attaqué {target.name} !")

        return target.take_damage(total_damage)

    def draw(
        self, x: int, y: int, surface: pygame.Surface, camera: tuple[int, int]
    ) -> None:
        super().draw(x, y, surface, camera)

        dest_x = x - camera[0]
        dest_y = y - camera[1]

        if self.draw_healthbar:
            self.healthbar.fill((255, 0, 0))
            self.healthbar.fill(
                (0, 255, 0),
                (
                    0,
                    0,
                    self.healthbar.get_width() * (self.health / self.max_health),
                    self.healthbar.get_height(),
                ),
            )
            surface.blit(self.healthbar, (dest_x, dest_y - 10))

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
