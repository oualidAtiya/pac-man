"""Owns the game window and the main loop."""

import pygame

from src.game.direction import Direction
from src.game.state import GameState, Screen
from src.ui.button import Button
from src.ui.hud import HUD
from time import time
class Renderer:
    """Owns the game window and drives the main event loop."""

    def __init__(
        self, width: int, height: int, fps: int = 60, title: str = "Pac-Man"
    ) -> None:
        """Initialize pygame and open the window. Called once at startup."""
        pygame.init()
        self.fps = fps
        self.delta_time = 0.0
        self.animation_time = 0.0
        self.width = width
        self.height = height
        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self._running = False
        self._menu_buttons = self._build_menu_buttons()
        self._pause_buttons = self._build_pause_buttons()
        self.hud = HUD()

    def _build_menu_buttons(self) -> dict[str, Button]:
        """Create and position the main menu's buttons, keyed by action name."""
        names = ["start", "high_scores", "instructions", "exit"]
        spacing = 32

        buttons = {name: Button(name=name) for name in names}
        total_height = sum(button.rect.height for button in buttons.values())
        total_height += (len(buttons) - 1) * spacing
        y = (self.height - total_height) // 2

        for button in buttons.values():
            button.rect.centerx = self.width // 2
            button.rect.top = y
            y += button.rect.height + spacing

        return buttons

    def _build_pause_buttons(self) -> dict[str, Button]:
        names = ["resume", "back"]
        spacing = 32

        buttons = {name: Button(name=name) for name in names}
        total_height = sum(button.rect.height for button in buttons.values())
        total_height += (len(buttons) - 1) * spacing
        y = (self.height) // 2

        for button in buttons.values():
            button.rect.centerx = self.width // 2
            button.rect.centery = y
            y += button.rect.height + spacing

        return buttons

    def is_lose(self, state: GameState) -> bool:
        if state.time_remaining == 0:
            return True
        return False

    def is_win(self, state: GameState) -> bool:
        if state.pacgum_counter == 0 and  state.level == 10 and state.time_remaining > 0:
            return True
        return False

    def run(self, state: GameState) -> None:
        """Run the main loop until a close condition is met.

        Blocks until the window is closed or Escape is pressed.
        """
        self._running = True
        clock = pygame.time.Clock()
        frames = 0
        while self._running:
            if self.is_lose(state):
                state.screen = Screen.GAME_OVER
                print("you lose time out.")
                return
            if self.is_win(state):
                state.screen = Screen.GAME_OVER
                print("you win: reach level 10 with eat all pacgums and still time")
                return
            if state.time_remaining > 0 and frames == 60:
               state.time_remaining -= 1
               frames = 0
            self.delta_time = clock.tick(self.fps) / 1000
            self.animation_time += self.delta_time
            self._handle_events(state)
            if state.screen == Screen.PLAYING:
                if state.player.dead_counter <= 0:
                    self.update(state)
                    state.update(self.delta_time)
                else:
                    state.player.dead_counter -= 1
            self._draw(state)
            frames += 1

        self._shutdown()

    def _handle_events(self, state: GameState) -> None:
        """Poll pending events once per frame and react to them."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key, state)

            elif event.type in [
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
            ]:
                self._handle_mouse(state, event)

    def _handle_keydown(self, key: int, state: GameState) -> None:
        """Handle a single keypress. Extend this as gameplay is added."""
        if key == pygame.K_ESCAPE:
            if state.screen == Screen.MENU:
                self._running = False
            elif state.screen == Screen.PLAYING:
                state.screen = Screen.PAUSED
            elif state.screen == Screen.PAUSED:
                state.screen = Screen.PLAYING
            elif (
                state.screen == Screen.INSTRUCTIONS
                or state.screen == Screen.HIGH_SCORES
            ):
                state.screen = Screen.MENU

        if state.screen == Screen.MENU:
            if key == pygame.K_RETURN:
                state.screen = Screen.PLAYING

        elif state.screen == Screen.PLAYING and state.player.dead_counter <= 0:
            if key == pygame.K_DOWN:
                state.player.request_move(Direction.SOUTH)
            if key == pygame.K_UP:
                state.player.request_move(Direction.NORTH)
            if key == pygame.K_RIGHT:
                state.player.request_move(Direction.EAST)
            if key == pygame.K_LEFT:
                state.player.request_move(Direction.WEST)

    def _handle_mouse(
        self, state: GameState, event: pygame.event.Event
    ) -> None:
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

        elif state.screen == Screen.PAUSED:
            if event.type == pygame.MOUSEMOTION:
                for button in self._pause_buttons.values():
                    button.handle_mouse_motion(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self._pause_buttons.values():
                    button.handle_mouse_down(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self._pause_buttons.values():
                    button.handle_mouse_up(state)

    def _draw(self, state: GameState) -> None:
        """Render exactly one frame based on the current game state."""
        self._screen.fill((39, 39, 54))
        if state.screen == Screen.MENU:
            self._draw_menu()
        elif state.screen == Screen.PLAYING:
            self._draw_gameplay(state)
        elif state.screen == Screen.PAUSED:
            self._draw_pause(state)
        elif state.screen == Screen.HIGH_SCORES:
            self._draw_high_scores()
        elif state.screen == Screen.INSTRUCTIONS:
            self._draw_instructions()
        elif state.screen == Screen.EXIT:
            self._running = False
        pygame.display.flip()

    def _draw_gameplay(self, state: GameState) -> None:
        self._draw_maze_pacgum(state)
        self.hud.draw(self._screen, state)
        self._draw_player(state)
        self._draw_ghosts(state)

    def _draw_pause(self, state: GameState) -> None:
        pause = pygame.image.load("assets/images/screens/pause.png")
        pause_rec = pause.get_rect()
        position = (
            self.width // 2 - pause_rec.width // 2,
            self.height // 2 - pause_rec.height // 2,
        )
        self._screen.blit(pause, position)

        for button in self._pause_buttons.values():
            button.draw(self._screen)

    def _draw_high_scores(self) -> None:
        high_scores = pygame.image.load(
            "assets/images/screens/high_scores.png"
        )
        high_scores_rect = high_scores.get_rect()
        position = (
            self.width // 2 - high_scores_rect.width // 2,
            self.height // 2 - high_scores_rect.height // 2,
        )
        self._screen.blit(high_scores, position)

    def _draw_instructions(self) -> None:
        instructions = pygame.image.load(
            "assets/images/screens/instructions.png"
        )
        instructions_rect = instructions.get_rect()
        position = (
            self.width // 2 - instructions_rect.width // 2,
            self.height // 2 - instructions_rect.height // 2,
        )
        self._screen.blit(instructions, position)

    def update(self, state: GameState) -> None:
        state.player.update_position()
        for ghost in state.ghosts:
            ghost.move(state)
            ghost.update_position()

    def _draw_maze_pacgum(self, state: GameState) -> None:
        state.maze.draw(self._screen)
        state.pacgum.draw(self._screen)

    def _draw_player(self, state: GameState) -> None:
        state.player.draw(self._screen)

    def _draw_ghosts(self, state: GameState) -> None:
        for ghost in state.ghosts:
            ghost.draw(self._screen, state, self.animation_time)

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
