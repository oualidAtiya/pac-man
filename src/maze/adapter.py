try:
    from mazegenerator import MazeGenerator
except ImportError:
    ...
from src.maze.cell import Cell
from src.config.models import GameConfig

class MazeAdapter:
    def __init__(self, config: GameConfig) -> None:
        self.width = config.width
        self.height = config.height
        self.seed = config.seed

    def generate_cell(self, cell_value: int) -> Cell:
        north = (cell_value & 1) != 0
        east = (cell_value & 2) != 0
        south = (cell_value & 4) != 0
        west = (cell_value & 8) != 0
        return Cell(north, east, west, south)

    def generate_maze(self) -> list[list[Cell]]:
        maze = MazeGenerator(size=(self.width, self.height), seed=self.seed).maze
        mapped_maze = []
        for row in maze:
            new_row = []
            for cell_value in row:
                new_row.append(self.generate_cell(cell_value)) 
            mapped_maze.append(new_row)
        return mapped_maze
