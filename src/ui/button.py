import pygame
from pygame.surface import Surface

from src.game.score import IO
from src.game.state import GameState, Screen
from src.ui.utils import Rectangle
from src.config.paths import resource_path


class Button:
    """A clickable menu button drawn from three pre-made images.

    The button has three visual states: normal, hover and pressed.
    A click is completed when the mouse is released on a button that
    was pressed, and the action is chosen from the button name.

    Attributes:
        width: Width of the button in pixels.
        heigh: Height of the button in pixels.
        rect: The rectangle giving the position and size of the button.
        state: The current visual state: "normal", "hover" or
            "pressed".
        name: The button name, which also selects its images and its
            action.
    """

    def __init__(self, name: str) -> None:
        """Load the three images of the button.

        The images are read from ``assets/images/buttons`` and are
        named ``<name>_normal.png``, ``<name>_hover.png`` and
        ``<name>_pressed.png``.

        Args:
            name: The button name, used as the image prefix and to
                choose the action done on click.
        """
        self._images = {
            "normal": pygame.image.load(
                resource_path(f"assets/images/buttons/{name}_normal.png")
            ).convert_alpha(),
            "hover": pygame.image.load(
                resource_path(f"assets/images/buttons/{name}_hover.png")
            ).convert_alpha(),
            "pressed": pygame.image.load(
                resource_path(f"assets/images/buttons/{name}_pressed.png")
            ).convert_alpha(),
        }
        self.width = 448
        self.heigh = 96
        self.rect = Rectangle(0, 0, self.width, self.heigh)
        self.state = "normal"
        self.name = name

    def reset_state(self) -> None:
        """Put the button back in its normal state."""
        self.state = "normal"

    def handle_mouse_motion(self, position: tuple[int, int]) -> None:
        """Update the hover state when the mouse moves.

        Nothing changes while the button is pressed.

        Args:
            position: The (x, y) position of the mouse.
        """
        if self.state != "pressed":
            collide = self.rect.collidepoint(position)
            self.state = "hover" if collide else "normal"

    def handle_mouse_down(self, position: tuple[int, int]) -> None:
        """Set the button as pressed if the mouse is pressed on it.

        Args:
            position: The (x, y) position of the mouse.
        """
        if self.rect.collidepoint(position):
            self.state = "pressed"

    def handle_mouse_up(self, state: GameState) -> None:
        """Run the button action when the mouse is released.

        Only a pressed button reacts. It goes back to its normal state,
        then the action depends on its name: start a new game, show the
        highscores (loading them first), show the instructions, resume
        the game, go back to the main menu, or exit.

        Args:
            state: The current game state, which is updated by the
                action.
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
        """Draw the button image that matches its current state.

        Args:
            screen: The surface to draw on.
        """
        screen.blit(self._images[self.state], tuple(self.rect))
