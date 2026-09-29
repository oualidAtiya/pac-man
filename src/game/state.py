from enum import Enum, auto

from src.game.ghost import Ghost, GhostBehavior
from src.game.player import Player
from src.maze.maze import Maze
from src.game.pacgum import Pacgum
from src.game.player import PacgumType

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
        self, maze: Maze, player: Player, ghosts: list[Ghost], pacgum: Pacgum
    ) -> None:
        self.screen = Screen.MENU
        self.maze = maze
        self.player = player
        self.ghosts = ghosts
        self.pacgum = pacgum
        self.level = 1
        self.time_remaining = 0.0

    def update(self):
        eaten = self.player.eat_current_cell()
        if eaten:
            if eaten == PacgumType.NORMAL:
                self.player.add_score(self.maze.config.points_per_pacgum)
            else:
                for ghost in self.ghosts:
                    ghost.set_behavior(GhostBehavior.FLEE)
                #TODO: collision logic
                self.player.add_score(self.maze.config.points_per_super_pacgum)
