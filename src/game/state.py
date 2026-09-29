from enum import Enum, auto

from src.game.ghost import Ghost, GhostBehavior
from src.game.pacgum import Pacgum
from src.game.player import PacgumType, Player
from src.maze.maze import Maze


class Screen(Enum):
    """Which screen/phase the game is currently in."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    HIGH_SCORES = auto()
    INSTRUCTIONS = auto()
    EXIT = auto()


class GameState:
    """Composition root: holds everything a frame needs to draw or
    update, without owning any of their logic itself.
    """

    def __init__(
        self,
        maze: Maze,
        player: Player,
        ghosts: list[Ghost],
        pacgum: Pacgum,
    ) -> None:
        self.screen = Screen.MENU
        self.maze = maze
        self.player = player
        self.ghosts = ghosts
        self.pacgum = pacgum
        self.level = 1
        self.time_remaining = 0.0
        self.super_pacgum_timer = 0.0

    def update(self, delta_time: float):
        eaten = self.player.eat_current_cell()

        if eaten == PacgumType.NORMAL:
            self.player.add_score(self.maze.config.points_per_pacgum)

        elif eaten == PacgumType.SUPER:
            self.super_pacgum_timer = self.pacgum.super_pacgum_duration

            for ghost in self.ghosts:
                ghost.set_behavior(GhostBehavior.FLEE)
            # TODO: collision logic
            self.player.add_score(self.maze.config.points_per_super_pacgum)

        if self.super_pacgum_timer > 0:
            self.super_pacgum_timer -= delta_time

            if self.super_pacgum_timer <= 0:
                for ghost in self.ghosts:
                    ghost.set_behavior(GhostBehavior.CHASE)

        p_col, p_row = self.player.position
        for ghost in self.ghosts:
            g_col, g_row = ghost.position_px
            difference = (abs(p_row-g_row), abs(p_col-g_col))
            if difference[0] <= 16 and difference[1] <= 16:
                if ghost.behavior == GhostBehavior.FLEE:
                    ghost.respawn()
                else:
                   if self.player.lose_life():
                       ...
                   self.player.respawn()
