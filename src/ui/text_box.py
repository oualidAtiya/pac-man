import string

import pygame
from pygame.surface import Surface

from src.ui.utils import Rectangle
from src.config.paths import resource_path


class TextBox:
    """A text box where the player types their name.

    The typed text is limited to 10 characters, and only letters,
    digits and spaces are accepted. The text is drawn with one image
    per character.

    Attributes:
        image: The image of the empty text box.
        letters: The character images, indexed by uppercase letter or
            digit.
        width: Width of the text box in pixels.
        height: Height of the text box in pixels.
        rect: The rectangle giving the position and size of the box.
        screen: The surface the box is drawn on.
        offset_y: Vertical offset of the box from the screen center.
        max_chars: The maximum number of characters allowed.
        value: The text typed so far.
    """

    def __init__(self, screen: Surface) -> None:
        """Load the images and create an empty text box.

        Args:
            screen: The surface the text box is drawn on.
        """
        self.image = pygame.image.load(
            resource_path("assets/images/text_boxes/text_box.png")
        )
        self.letters = {
            letter: pygame.image.load(
                resource_path(f"assets/images/letters/{letter}.png")
            )
            for letter in [*string.digits, *string.ascii_uppercase]
        }
        self.width = 576
        self.height = 92
        self.rect = Rectangle(0, 0, self.width, self.height)
        self.screen = screen
        self.offset_y = 174
        self.max_chars = 10
        self.value = ""

    def reset(self) -> None:
        """Clear the typed text."""
        self.value = ""

    def add_char(self, char: str) -> None:
        """Add a character to the text if it is allowed.

        The character is ignored when the text already has the maximum
        length, or when it is not a letter, a digit or a space.

        Args:
            char: The character typed by the player.
        """
        if len(self.value) < self.max_chars:
            self.value += char if char.isalnum() or char == " " else ""

    def remove_char(self) -> None:
        """Remove the last character of the text, if there is one."""
        self.value = self.value[:-1]

    def draw(self) -> None:
        """Draw the text box and the text typed inside it."""
        self.screen.blit(self.image, tuple(self.rect))
        self.draw_text()

    def draw_text(self) -> None:
        """Draw the typed text, one character image at a time.

        The rectangle is moved while drawing, so that each character
        is placed after the previous one.
        """
        self.rect.centery += 32
        self.rect.centerx += 92
        for char in self.value:
            if char == " ":
                self.rect.centerx += 32
            else:
                image = self.letters[char.upper()]
                self.rect.centerx += 32
                self.screen.blit(image, tuple(self.rect))
