from src.config.models import GameConfig
from src.maze.adapter import MazeAdapter


class Maze:
    def __init__(self, config: GameConfig) -> None:
        self.grid = MazeAdapter(config).generate_maze()
        self.config = config
