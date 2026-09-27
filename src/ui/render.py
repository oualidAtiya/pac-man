"""Owns the game window and the main loop."""

import pygame
from src.game.direction import Direction
from src.game.state import GameState, Screen
from src.ui.button import Button


class Renderer:
    """Owns the game window and drives the main event loop."""

    def __init__(
        self, width: int, height: int, title: str = "Pac-Man"
    ) -> None:
        """Initialize pygame and open the window. Called once at startup."""
        pygame.init()
        self.width = width
        self.height = height
        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self._running = False
        self._menu_buttons = self._build_menu_buttons()

    def _build_menu_buttons(self) -> dict[str, Button]:
        """Create and position the main menu's buttons, keyed by action name."""
        names = ["start", "high_scores", "instructions", "exit"]
        spacing = 32

        buttons = {name: Button((0, 0), name) for name in names}
        total_height = sum(button.rect.height for button in buttons.values())
        total_height += (len(buttons) - 1) * spacing
        y = (self.height - total_height) // 2

        for button in buttons.values():
            button.rect.centerx = self.width // 2
            button.rect.top = y
            y += button.rect.height + spacing

        return buttons

    def run(self, state: GameState) -> None:
        """Run the main loop until a close condition is met.

        Blocks until the window is closed or Escape is pressed.
        """
        self._running = True
        clock = pygame.time.Clock()

        while self._running:
            self._handle_events(state)
            state.player.update_position()
            self._draw(state)
            clock.tick(60)

        self._shutdown()

    def _handle_events(self, state: GameState) -> None:
        """Poll pending events once per frame and react to them."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key, state)

            if state.screen == Screen.MENU:
                if event.type == pygame.MOUSEMOTION:
                    for button in self._menu_buttons.values():
                        button.handle_mouse_motion(event.pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self._menu_buttons.values():
                        button.handle_mouse_down(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    for button in self._menu_buttons.values():
                        button.handle_mouse_up(state)

    def _handle_keydown(self, key: int, state: GameState) -> None:
        """Handle a single keypress. Extend this as gameplay is added."""
        if key == pygame.K_ESCAPE:
            if state.screen == Screen.MENU:
                self._running = False
            elif state.screen != Screen.MENU:
                state.screen = Screen.MENU

        if state.screen == Screen.PLAYING:
            if key == pygame.K_DOWN:
                state.player.request_move(Direction.SOUTH)
            if key == pygame.K_UP:
                state.player.request_move(Direction.NORTH)
            if key == pygame.K_RIGHT:
                state.player.request_move(Direction.EAST)
            if key == pygame.K_LEFT:
                state.player.request_move(Direction.WEST)

    def _draw(self, state: GameState) -> None:
        """Render exactly one frame based on the current game state."""
        self._screen.fill((39, 39, 54))
        if state.screen == Screen.MENU:
            self._draw_menu()
        elif state.screen == Screen.PLAYING:
            self._draw_gameplay(state)
        elif state.screen == Screen.EXIT:
            self._running = False
        pygame.display.flip()

    def _draw_gameplay(self, state: GameState) -> None:
        state.maze.draw(self._screen)
        state.pacgum.draw(self._screen)
        state.player.draw(self._screen)

    def _draw_menu(self) -> None:
        self._draw_title()
        for button in self._menu_buttons.values():
            button.draw(self._screen)

    def _draw_title(self) -> None:
        title = pygame.image.load("assets/images/title.png")
        title_rect = title.get_rect()
        title_rect.centerx = self.width // 2
        title_rect.top += 192
        self._screen.blit(title, title_rect)

        sub_title = pygame.image.load("assets/images/subtitle.png")
        sub_title_rect = sub_title.get_rect()
        sub_title_rect.centerx = self.width // 2
        sub_title_rect.top += title_rect.height + 272
        self._screen.blit(sub_title, sub_title_rect)

    def _shutdown(self) -> None:
        """Release pygame resources so no window or process is left hanging."""
        pygame.quit()
