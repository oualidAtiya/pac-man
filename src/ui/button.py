"""Mouse-driven menu button: pre-sized images, no runtime scaling or fonts."""

import pygame
from pygame.surface import Surface
from src.game.score import IO
from src.game.state import GameState, Screen
from src.ui.utils import Rectangle


class Button:
    """A single menu button using pre-baked normal/hover/pressed images."""

    def __init__(self, name: str) -> None:
        """Initialize a button using the specified asset prefix.

        Args:
            name: Prefix used to locate the button's image assets.
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
        self.width = 448
        self.heigh = 96
        self.rect = Rectangle(0, 0, self.width, self.heigh)
        self.state = "normal"
        self.name = name

    def reset_state(self) -> None:
        """Reset the button to its normal state."""

    def handle_mouse_motion(self, position: tuple[int, int]) -> None:
        """Update the button state based on the mouse position.

        Args:
            position: Current mouse position as an x and y coordinate.
        """
        if self.state != "pressed":
            collide = self.rect.collidepoint(position)
            self.state = "hover" if collide else "normal"

    def handle_mouse_down(self, position: tuple[int, int]) -> None:
        """Set the button to pressed when clicked.

        Args:
            position: Mouse position as an x and y coordinate.
        """
        if self.rect.collidepoint(position):
            self.state = "pressed"

    def handle_mouse_up(self, state: GameState) -> None:
        """Handle the action associated with the released button.

        Args:
            state: Current game state to update.
        """
        if self.state != "pressed":
            return

        self.reset_state()
        match self.name:
            case "start":
                state.reset(False)
                state.screen = Screen.PLAYING
            case "high_scores":
                state.screen = Screen.HIGH_SCORES
                state.scores = IO(state.maze.config.highscore_filename).load()
            case "instructions":
                state.screen = Screen.INSTRUCTIONS
            case "resume":
                state.screen = Screen.PLAYING
            case "back":
                state.screen = Screen.MENU
            case "exit":
                state.screen = Screen.EXIT

    def draw(self, screen: Surface) -> None:
        """Draw the button on the provided screen.

        Args:
            screen: Surface on which to draw the button.
        """
        screen.blit(self._images[self.state], tuple(self.rect))
