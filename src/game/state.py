from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from src.game.ghost import Ghost, GhostBehavior
from src.game.pacgum import Pacgum, PacgumType
from src.ui.text_box import TextBox
from src.game.score import Score

if TYPE_CHECKING:
    from src.game.player import Player
from src.maze.maze import Maze


class Screen(Enum):
    """The screens or phases the game can be in.

    Attributes:
        MENU: The main menu.
        PLAYING: A game is running.
        PAUSED: The game is paused.
        GAME_OVER: The player lost all lives.
        VICTORY: The player completed all levels.
        HIGH_SCORES: The highscores list is displayed.
        INSTRUCTIONS: The controls and rules are displayed.
        EXIT: The game must close.
    """

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    HIGH_SCORES = auto()
    INSTRUCTIONS = auto()
    EXIT = auto()


class GameState:
    """Hold everything needed to update and draw a frame of the game.

    It groups the maze, the player, the ghosts and the pacgums, and
    contains the rules that link them together (eating gums, ghost
    collisions, level changes).

    Attributes:
        screen: The screen or phase the game is currently in.
        maze: The maze of the current level.
        player: The player.
        ghosts: The four ghosts.
        pacgum: The gums of the current level.
        level: The current level number, starting at 1.
        time_remaining: Time left in the current level, in seconds.
        super_pacgum_timer: Seconds left while ghosts are edible.
        check_colission: Whether collisions with ghosts are checked.
        scores: The list of highscores.
    """

    def __init__(
        self,
        maze: Maze,
        player: Player,
        ghosts: list[Ghost],
        pacgum: Pacgum,
    ) -> None:
        """Create the game state, starting on the main menu.

        Args:
            maze: The maze of the first level.
            player: The player.
            ghosts: The four ghosts.
            pacgum: The gums placed in the maze.
        """
        self.screen = Screen.MENU
        self.maze = maze
        self.player = player
        self.ghosts = ghosts
        self.pacgum = pacgum
        self.level = 1
        self.time_remaining = maze.config.level_max_time
        self.super_pacgum_timer = 0.0
        self.check_colission = True
        self.scores: list[Score] = []

    def respawn_all_ghosts(self) -> None:
        """Send every ghost back to its spawn cell."""
        for ghost in self.ghosts:
            ghost.respawn()

    def next_level(self) -> None:
        """Move to the next level if the last one is not reached.

        The level is rebuilt with a new maze, then the level number is
        increased. Nothing happens when the level is already 10.
        """
        if self.level < 10:
            self.reset(True)
            self.level += 1

    def reset(self, next_level: bool) -> None:
        """Rebuild the maze, gums, player and ghosts.

        When ``next_level`` is False, the game restarts from level 1
        with a score of 0 and full lives. In both cases a new maze is
        generated, the gums are placed again, the ghosts return to the
        four corners in chase mode, and the timers are reset.

        Args:
            next_level: True when moving on to the next level, False
                when starting a new game.
        """
        if not next_level:
            self.level = 1
            self.player.score = 0
            self.player.lives = self.maze.config.lives
        self.maze.regenerate_maze(next_level)
        self.player.maze = self.maze
        self.player.set_attr()
        self.player.respawn()
        self.pacgum = Pacgum(self.maze)
        self.ghosts[0].set_position((0, 0))
        self.ghosts[1].set_position((self.maze.config.width - 1, 0))
        self.ghosts[2].set_position((0, self.maze.config.height - 1))
        self.ghosts[3].set_position(
            (self.maze.config.width - 1, self.maze.config.height - 1)
        )
        self.respawn_all_ghosts()
        self.time_remaining = self.maze.config.level_max_time
        self.super_pacgum_timer = 0.0

        for ghost in self.ghosts:
            ghost.set_behavior(GhostBehavior.CHASE)

    def update(self, delta_time: float, text_box: TextBox) -> None:
        """Apply the game rules for one frame.

        Handles, in order: eating the gum on the player's cell and
        scoring it, going to the next level when no pacgum is left,
        the super-pacgum timer (ghosts return to chase mode when it
        ends), and collisions between the player and the ghosts. An
        edible ghost that is touched gives points and respawns, any
        other ghost makes the player lose a life, or ends the game
        when no life is left.

        Args:
            delta_time: Time elapsed since the last frame, in seconds.
            text_box: The name input box, reset when the game is over.
        """
        eaten = self.player.eat_current_cell()
        if eaten == PacgumType.NORMAL:
            self.player.add_score(self.maze.config.points_per_pacgum)
            self.pacgum.pacgum_counter -= 1

        elif eaten == PacgumType.SUPER:
            self.super_pacgum_timer = self.pacgum.super_pacgum_duration
            for ghost in self.ghosts:
                ghost.set_behavior(GhostBehavior.FLEE)
            self.player.add_score(self.maze.config.points_per_super_pacgum)

        if self.pacgum.pacgum_counter == 0:
            self.next_level()
            return

        if self.super_pacgum_timer > 0:
            self.super_pacgum_timer -= delta_time

            if self.super_pacgum_timer <= 0:
                for ghost in self.ghosts:
                    ghost.set_behavior(GhostBehavior.CHASE)
        if self.check_colission:
            p_col, p_row = self.player.position
            for ghost in self.ghosts:
                g_col, g_row = ghost.position_px
                difference = (abs(p_row - g_row), abs(p_col - g_col))

                if difference[0] <= 28 and difference[1] <= 28:
                    if ghost.behavior == GhostBehavior.FLEE:
                        self.player.add_score(
                            self.maze.config.points_per_ghost
                        )
                        ghost.respawn()
                    else:
                        if self.player.lose_life():
                            self.screen = Screen.GAME_OVER
                            text_box.reset()
                            break
                        self.player.dead_counter = 120
                        self.player.dead_position = self.player.position
                        self.respawn_all_ghosts()
                        self.player.respawn()
                        break
