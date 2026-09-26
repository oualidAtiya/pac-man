"""Mouse-driven menu button: pre-sized images, no runtime scaling or fonts."""

import pygame
from pygame.surface import Surface

from src.game.state import GameState, Screen


class Button:
    """A single menu button using pre-baked normal/hover/pressed images."""

    def __init__(self, position: tuple[int, int], name: str) -> None:
        """`name` is the button's asset prefix, e.g. 'start' loads
        assets/start_normal.png, assets/start_hover.png, assets/start_pressed.png.
        """
        self._images = {
            "normal": pygame.image.load(
                f"assets/images/buttons/{name}_normal.png"
            ).convert_alpha(),
            "hover": pygame.image.load(
                f"assets/images/buttons/{name}_hover.png"
            ).convert_alpha(),
            "pressed": pygame.image.load(
                f"assets/images/buttons/{name}_pressed.png"
            ).convert_alpha(),
        }
        self.rect = self._images["normal"].get_rect()
        self.state = "normal"
        self.name = name

    def handle_mouse_motion(self, position: tuple[int, int]) -> None:
        if self.state != "pressed":
            self.state = (
                "hover" if self.rect.collidepoint(position) else "normal"
            )

    def handle_mouse_down(self, position: tuple[int, int]) -> bool:
        if self.rect.collidepoint(position):
            self.state = "pressed"
            return True
        return False

    def on_button_pressed(self, state: GameState) -> None:
        if self.name == "start":
            state.screen = Screen.PLAYING
        if self.name == "high_scores":
            state.screen = Screen.HIGH_SCORES
        if self.name == "instructions":
            state.screen = Screen.INSTRUCTIONS
        if self.name == "exit":
            state.screen = Screen.EXIT

    def handle_mouse_up(self, position: tuple[int, int]) -> None:
        self.state = "hover" if self.rect.collidepoint(position) else "normal"

    def draw(self, screen: Surface) -> None:
        screen.blit(self._images[self.state], self.rect)
