"""Owns the game window and the main loop."""

import pygame

from src.game.direction import Direction
from src.game.state import GameState, Screen
from src.ui.button import Button
from src.ui.hud import HUD
from src.ui.text_box import TextBox


class Renderer:
    """Owns the game window and drives the main event loop."""

    def __init__(
        self, width: int, height: int, fps: int = 60, title: str = "Pac-Man"
    ) -> None:
        """Initialize pygame and open the window. Called once at startup."""
        pygame.init()
        pygame.display.set_caption(title)
        self._screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load(
            "assets/images/background.png"
        ).convert_alpha()

        self.fps = fps
        self.width = width
        self.height = height
        self._running = False
        self.delta_time = 0.0
        self.animation_time = 0.0

        self._menu_buttons = self._build_menu_buttons()
        self._pause_buttons = self._build_pause_buttons()
        self.text_box = TextBox(self._screen)
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

    def run(self, state: GameState) -> None:
        """Run the main loop until a close condition is met.

        Blocks until the window is closed or Escape is pressed.
        """
        self._running = True
        clock = pygame.time.Clock()
        frames = 0
        while self._running:
            if state.player.is_lose(state):
                state.screen = Screen.GAME_OVER

            if state.player.is_win(state):
                state.screen = Screen.VICTORY

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
                self._handle_keydown(event.key, event, state)

            elif event.type in [
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
            ]:
                self._handle_mouse(state, event)

    def _handle_keydown(
        self, key: int, event: pygame.event.Event, state: GameState
    ) -> None:
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

        elif state.screen == Screen.MENU:
            if key == pygame.K_RETURN:
                state.screen = Screen.PLAYING

        elif state.screen == Screen.PLAYING and state.player.dead_counter <= 0:
            if key == pygame.K_t:
                state.time_remaining += 10
            if key == pygame.K_w:
                state.pacgum.pacgum_counter = 0
            if key == pygame.K_c:
                state.check_colission = not state.check_colission

            if key == pygame.K_DOWN:
                state.player.request_move(Direction.SOUTH)
            if key == pygame.K_UP:
                state.player.request_move(Direction.NORTH)
            if key == pygame.K_RIGHT:
                state.player.request_move(Direction.EAST)
            if key == pygame.K_LEFT:
                state.player.request_move(Direction.WEST)

        elif (
            state.screen == Screen.VICTORY or state.screen == Screen.GAME_OVER
        ):
            if key == pygame.K_BACKSPACE:
                self.text_box.value = self.text_box.value[:-1]
            else:
                char = event.unicode
                if len(self.text_box.value) < self.text_box.max_chars:
                    self.text_box.value += (
                        char if char.isalnum() or char == " " else ""
                    )

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
        self._screen.blit(self.background, (0, 0))

        match state.screen:
            case Screen.MENU:
                self._draw_menu()
            case Screen.PLAYING:
                self._draw_gameplay(state)
            case Screen.PAUSED:
                self._draw_pause(state)
            case Screen.HIGH_SCORES:
                self._draw_high_scores()
            case Screen.INSTRUCTIONS:
                self._draw_instructions()
            case Screen.VICTORY:
                self._draw_victory()
            case Screen.GAME_OVER:
                self._draw_game_over()
            case Screen.EXIT:
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

    def _draw_victory(self) -> None:
        victory = pygame.image.load("assets/images/screens/victory.png")
        victory_rect = victory.get_rect()
        position = (
            self.width // 2 - victory_rect.width // 2,
            self.height // 2 - victory_rect.height // 2,
        )
        self._screen.blit(victory, position)

        self.text_box.rect.centerx = self.width // 2
        self.text_box.rect.centery = self.height // 2
        self.text_box.rect.centery += self.text_box.offset_y

        self.text_box.draw()

    def _draw_game_over(self) -> None:
        game_over = pygame.image.load("assets/images/screens/game_over.png")
        game_over_rect = game_over.get_rect()
        position = (
            self.width // 2 - game_over_rect.width // 2,
            self.height // 2 - game_over_rect.height // 2,
        )
        self._screen.blit(game_over, position)

        offset_y = 174
        self.text_box.rect.centerx = self.width // 2
        self.text_box.rect.centery = self.height // 2
        self.text_box.rect.centery += offset_y

        self.text_box.draw()

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

    def _shutdown(self) -> None:
        """Release pygame resources so no window or process is left hanging."""
        pygame.quit()
