from src.config.logger import logger

try:
    from mazegenerator import MazeGenerator
except ImportError:
    logger.error("Can't import 'MazeGenerator'")
from src.config.models import GameConfig
from src.maze.cell import Cell


class MazeAdapter:
    def __init__(self, config: GameConfig) -> None:
        self.width = config.width
        self.height = config.height
        self.seed = config.seed

    def generate_cell(self, cell_value: int) -> Cell:
        return Cell(cell_value)

    def generate_maze(self) -> list[list[Cell]]:
        maze = MazeGenerator(
            size=(self.width, self.height), seed=self.seed
        ).maze
        mapped_maze = []
        for row in maze:
            new_row = []
            for cell_value in row:
                new_row.append(self.generate_cell(cell_value))
            mapped_maze.append(new_row)
        return mapped_maze
