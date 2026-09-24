from enum import Enum, auto

from src.maze.maze import Maze

from src.game.ghost import Ghost
from src.game.player import Player


class Screen(Enum):
    """Which screen/phase the game is currently in."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class GameState:
    """Composition root: holds everything a frame needs to draw or
    update, without owning any of their logic itself.
    """

    def __init__(
        self, maze: Maze, player: Player, ghosts: list[Ghost]
    ) -> None:
        self.screen = Screen.MENU
        self.maze = maze
        self.player = player
        self.ghosts = ghosts
        self.score = 0
        self.lives = 3
        self.level = 1
        self.time_remaining = 0.0
