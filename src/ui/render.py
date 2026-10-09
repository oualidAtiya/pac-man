import pygame

from src.game.direction import Direction
from src.game.ghost import GhostBehavior
from src.game.score import IO, Score
from src.game.state import GameState, Screen
from src.ui.button import Button
from src.ui.hud import HUD
from src.ui.text_box import TextBox
from src.ui.utils import Rectangle
from src.config.paths import resource_path


class Renderer:
    """Own the game window, run the main loop and draw every screen.

    It reads the keyboard and mouse events, updates the game while it
    is playing, and draws the screen that matches the current state.

    Attributes:
        background: The background image drawn on every frame.
        fps: The maximum number of frames per second.
        width: Width of the window in pixels.
        height: Height of the window in pixels.
        delta_time: Seconds elapsed during the last frame.
        animation_time: Total seconds elapsed, used for animations.
        current_frame: Frame counter used to count one second.
        text_box: The text box used to type the player name.
        hud: The heads-up display shown during the game.
    """

    def __init__(
        self, width: int, height: int, fps: int = 60, title: str = "Pac-Man"
    ) -> None:
        """Initialize pygame, open the window and build the UI.

        Args:
            width: Width of the window in pixels.
            height: Height of the window in pixels.
            fps: The maximum number of frames per second.
            title: The title of the window.
        """
        pygame.init()
        pygame.display.set_caption(title)
        self._screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load(
            resource_path("assets/images/background.png")
        ).convert_alpha()

        self.fps = fps
        self.width = width
        self.height = height
        self._running = False
        self.delta_time = 0.0
        self.animation_time = 0.0
        self.current_frame = 0
        self._menu_buttons = self._build_menu_buttons()
        self._pause_buttons = self._build_pause_buttons()
        self.text_box = TextBox(self._screen)
        self.hud = HUD()

    def _build_menu_buttons(self) -> dict[str, Button]:
        """Create the main menu buttons and center them vertically.

        Returns:
            The buttons of the main menu, indexed by their name.
        """
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
        """Create the pause menu buttons and place them on screen.

        Returns:
            The buttons of the pause menu, indexed by their name.
        """
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

    def handle_delay(self, state: GameState) -> None:
        """Count frames and remove one second from the level timer.

        Args:
            state: The current game state, whose timer is updated.
        """
        if state.time_remaining > 0 and self.current_frame == 60:
            state.time_remaining -= 1
            self.current_frame = 0
        self.current_frame += 1

    def check_time(self, state: GameState) -> None:
        """Handle the end of the level timer.

        When the time is over, the player loses a life. The game ends
        if no life is left, otherwise the player and ghosts respawn
        and the timer restarts.

        Args:
            state: The current game state.
        """
        if state.player.is_time_out(state):
            if state.player.lose_life():
                state.screen = Screen.GAME_OVER
                self.text_box.reset()
                return
            state.player.dead_counter = 120
            state.player.dead_position = state.player.position
            state.respawn_all_ghosts()
            state.player.respawn()
            state.time_remaining = state.maze.config.level_max_time

    def run(self, state: GameState) -> None:
        """Run the main loop until the game is closed.

        On each frame it checks the timer and the victory condition,
        handles the events, updates the game while playing, and draws
        the screen. Pygame is shut down when the loop ends.

        Args:
            state: The current game state.
        """
        self._running = True
        clock = pygame.time.Clock()
        while self._running:
            self.check_time(state)
            if state.player.is_win(state):
                state.screen = Screen.VICTORY
                self.text_box.reset()
                state.level = 1

            self.delta_time = clock.tick(self.fps) / 1000
            self.animation_time += self.delta_time
            self._handle_events(state)

            if state.screen == Screen.PLAYING:
                if state.player.dead_counter <= 0:
                    self.handle_delay(state)
                    self.update(state)
                    state.update(self.delta_time, self.text_box)
                else:
                    state.player.dead_counter -= 1
            self._draw(state)

        self._shutdown()

    def _handle_events(self, state: GameState) -> None:
        """Read the pending pygame events and dispatch them.

        Args:
            state: The current game state.
        """
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
        """React to a key press according to the current screen.

        Escape quits from the menu, toggles the pause while playing and
        goes back to the menu elsewhere. Enter starts a new game from
        the menu. While playing, the arrow keys move the player and the
        cheat keys are available: T adds 10 seconds, W wins the level,
        C toggles ghost collisions and S makes ghosts edible. On the
        victory and game over screens, the keys edit the player name
        and Enter saves the score.

        Args:
            key: The pygame key code that was pressed.
            event: The key event, used to read the typed character.
            state: The current game state.
        """
        if key == pygame.K_ESCAPE:
            if state.screen == Screen.MENU:
                self._running = False
            elif state.screen == Screen.PLAYING:
                state.screen = Screen.PAUSED
            elif state.screen == Screen.PAUSED:
                state.screen = Screen.PLAYING
            else:
                state.screen = Screen.MENU

        if state.screen == Screen.MENU:
            if key == pygame.K_RETURN:
                state.reset(False)
                state.screen = Screen.PLAYING

        elif state.screen == Screen.PLAYING and state.player.dead_counter <= 0:
            if key == pygame.K_t:
                state.time_remaining += 10
            if key == pygame.K_w:
                state.pacgum.pacgum_counter = 0
            if key == pygame.K_c:
                state.check_colission = not state.check_colission
            if key == pygame.K_s:
                for ghost in state.ghosts:
                    ghost.set_behavior(GhostBehavior.FLEE)

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
            if (
                key == pygame.K_RETURN
                and not self.text_box.value.isspace()
                and self.text_box.value
            ):
                IO(state.maze.config.highscore_filename).save(
                    score=Score(
                        name=self.text_box.value,
                        score=state.player.score,
                    )
                )
                state.screen = Screen.MENU

            elif key == pygame.K_BACKSPACE:
                self.text_box.remove_char()

            else:
                char = event.unicode
                self.text_box.add_char(char)

    def _handle_mouse(
        self, state: GameState, event: pygame.event.Event
    ) -> None:
        """Send a mouse event to the buttons of the visible menu.

        Only the main menu and the pause menu have buttons.

        Args:
            state: The current game state.
            event: The mouse event (motion, press or release).
        """
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
        """Draw one frame for the current screen and show it.

        Args:
            state: The current game state.
        """
        self._screen.blit(self.background, (0, 0))

        match state.screen:
            case Screen.MENU:
                self._draw_menu()
            case Screen.PLAYING:
                self._draw_gameplay(state)
            case Screen.PAUSED:
                self._draw_pause(state)
            case Screen.HIGH_SCORES:
                self._draw_high_scores(state)
            case Screen.INSTRUCTIONS:
                self._draw_instructions()
            case Screen.VICTORY:
                self._draw_victory(state)
            case Screen.GAME_OVER:
                self._draw_game_over(state)
            case Screen.EXIT:
                self._running = False

        pygame.display.flip()

    def _draw_gameplay(self, state: GameState) -> None:
        """Draw the maze, gums, HUD, player and ghosts.

        Args:
            state: The current game state.
        """
        self._draw_maze_pacgum(state)
        self.hud.draw(self._screen, state)
        self._draw_player(state)
        self._draw_ghosts(state)

    def _draw_pause(self, state: GameState) -> None:
        """Draw the pause panel and its buttons.

        Args:
            state: The current game state (not used here).
        """
        pause = pygame.image.load(
            resource_path("assets/images/screens/pause.png")
        )
        width = 768
        height = 584
        pause_rec = Rectangle(0, 0, width, height)
        position = (
            self.width // 2 - pause_rec.width // 2,
            self.height // 2 - pause_rec.height // 2,
        )
        self._screen.blit(pause, position)

        for button in self._pause_buttons.values():
            button.draw(self._screen)

    def _draw_high_scores(self, state: GameState) -> None:
        """Draw the highscores panel with the top 10 names and scores.

        Names and scores are drawn letter by letter with the images of
        the text box font.

        Args:
            state: The current game state, which holds the scores.
        """
        high_scores = pygame.image.load(
            resource_path("assets/images/screens/high_scores.png")
        )
        width = 1280
        height = 960
        high_scores_rect = Rectangle(0, 0, width, height)
        position = (
            self.width // 2 - high_scores_rect.width // 2,
            self.height // 2 - high_scores_rect.height // 2,
        )
        self._screen.blit(high_scores, position)

        name_offset_x, name_offset_y = 330, 292
        name_x, name_y = (
            position[0] + name_offset_x,
            position[1] + name_offset_y,
        )
        score_offset_x, score_offset_y = 800, 292
        score_x, score_y = (
            position[0] + score_offset_x,
            position[1] + score_offset_y,
        )
        for score in state.scores[:10]:
            name_x = position[0] + name_offset_x
            for char in score.name:
                if char == " ":
                    name_x += 32
                else:
                    imgae = self.text_box.letters[char.upper()]
                    self._screen.blit(imgae, (name_x, name_y))
                    name_x += 32
            name_y += 48

            score_x = position[0] + score_offset_x
            for char in str(score.score):
                imgae = self.text_box.letters[char]
                self._screen.blit(imgae, (score_x, score_y))
                score_x += 32
            score_y += 48

    def _draw_instructions(self) -> None:
        """Draw the instructions panel with the controls and rules."""
        instructions = pygame.image.load(
            resource_path("assets/images/screens/instructions.png")
        )
        width, height = 1280, 960
        instructions_rect = Rectangle(0, 0, width, height)
        position = (
            self.width // 2 - instructions_rect.width // 2,
            self.height // 2 - instructions_rect.height // 2,
        )
        self._screen.blit(instructions, position)

    def update(self, state: GameState) -> None:
        """Move the player and the ghosts for one frame.

        Args:
            state: The current game state.
        """
        state.player.update_position()
        for ghost in state.ghosts:
            ghost.move(state)
            ghost.update_position()

    def _draw_maze_pacgum(self, state: GameState) -> None:
        """Draw the maze walls and the gums.

        Args:
            state: The current game state.
        """
        state.maze.draw(self._screen)
        state.pacgum.draw(self._screen)

    def _draw_player(self, state: GameState) -> None:
        """Draw the player.

        Args:
            state: The current game state.
        """
        state.player.draw(self._screen)

    def _draw_ghosts(self, state: GameState) -> None:
        """Draw all the ghosts.

        Args:
            state: The current game state.
        """
        for ghost in state.ghosts:
            ghost.draw(self._screen, state, self.animation_time)

    def _draw_victory(self, state: GameState) -> None:
        """Draw the victory panel, the final score and the name box.

        Args:
            state: The current game state.
        """
        victory = pygame.image.load(
            resource_path("assets/images/screens/victory.png")
        )
        width = 1280
        height = 960
        victory_rect = Rectangle(0, 0, width, height)
        position = (
            self.width // 2 - victory_rect.width // 2,
            self.height // 2 - victory_rect.height // 2,
        )
        self._screen.blit(victory, position)
        self.text_box.rect.centerx = self.width // 2
        self.text_box.rect.centery = self.height // 2
        self.text_box.rect.centery += self.text_box.offset_y

        self.draw_score(state, position, victory_rect)
        self.text_box.draw()

    def _draw_game_over(self, state: GameState) -> None:
        """Draw the game over panel, the final score and the name box.

        Args:
            state: The current game state.
        """
        game_over = pygame.image.load(
            resource_path("assets/images/screens/game_over.png")
        )
        width = 1280
        height = 960
        game_over_rect = Rectangle(0, 0, width, height)
        position = (
            self.width // 2 - game_over_rect.width // 2,
            self.height // 2 - game_over_rect.height // 2,
        )
        self._screen.blit(game_over, position)

        offset_y = 174
        self.text_box.rect.centerx = self.width // 2
        self.text_box.rect.centery = self.height // 2
        self.text_box.rect.centery += offset_y

        self.draw_score(state, position, game_over_rect)
        self.text_box.draw()

    def draw_score(
        self,
        state: GameState,
        screen_position: tuple[int, int],
        screen_rec: Rectangle,
    ) -> None:
        """Draw the player's score, centered on a panel.

        Each digit is drawn with the image of the text box font.

        Args:
            state: The current game state, which holds the score.
            screen_position: The top-left (x, y) of the panel.
            screen_rec: The rectangle giving the size of the panel.
        """
        score = str(state.player.score)
        score_len = len(score) * 32
        x, y = (
            (screen_position[0] + (screen_rec.width // 2)) - score_len // 2,
            screen_position[1] + screen_rec.height // 2 - 32,
        )
        for char in score:
            digit = self.text_box.letters[char]
            self._screen.blit(digit, (x, y))
            x += 32

    def _draw_menu(self) -> None:
        """Draw the main menu: the title and the buttons."""
        self._draw_title()
        for button in self._menu_buttons.values():
            button.draw(self._screen)

    def _draw_title(self) -> None:
        """Draw the game title image at the top of the menu."""
        title = pygame.image.load(resource_path("assets/images/title.png"))
        width, height = 736, 112
        title_rect = Rectangle(0, 0, width, height)
        title_rect.centerx = self.width // 2
        title_rect.top += 192
        self._screen.blit(title, tuple(title_rect))

    def _shutdown(self) -> None:
        """Close pygame so no window or process stays open."""
        pygame.quit()
