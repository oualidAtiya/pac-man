import string

import pygame
from pygame.surface import Surface


class TextBox:
    def __init__(self, screen: Surface) -> None:
        self.image = pygame.image.load("assets/images/text_boxes/text_box.png")
        self.letters = {
            letter: pygame.image.load(f"assets/images/letters/{letter}.png")
            for letter in [*string.digits, *string.ascii_uppercase]
        }
        self.rect = self.image.get_rect()
        self.screen = screen
        self.offset_y = 174
        self.max_chars = 10
        self.value = ""

    def reset(self) -> None:
        self.value = ""

    def add_char(self, char: str) -> None:
        if len(self.value) < self.max_chars:
            self.value += char if char.isalnum() or char == " " else ""

    def remove_char(self) -> None:
        self.value = self.value[:-1]

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
        self.draw_text()

    def draw_text(self) -> None:
        self.rect.centery += 32
        self.rect.centerx += 92
        for char in self.value:
            if char == " ":
                self.rect.centerx += 32
            else:
                image = self.letters[char.upper()]
                self.rect.centerx += 32
                self.screen.blit(image, self.rect)
