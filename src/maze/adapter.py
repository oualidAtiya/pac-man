from src.config.logger import logger
try:
    from mazegenerator import MazeGenerator
except ImportError:
    logger.error("Can't import 'MazeGenerator'")
from src.config.models import GameConfig
from src.maze.cell import Cell


class MazeAdapter:
    """Adapt the assigned A-Maze-ing package to the game's own cells.

    The package returns a grid of raw integer values. This class
    converts each value into a ``Cell`` object that the rest of the
    game can use.

    Attributes:
        width: Width of the maze to generate.
        height: Height of the maze to generate.
        seed: Seed given to the generator.
    """

    def __init__(self, config: GameConfig) -> None:
        """Store the generation parameters taken from the config.

        Args:
            config: The game configuration, used for the maze width,
                height and seed.
        """
        self.width = config.width
        self.height = config.height
        self.seed = config.seed

    def generate_cell(self, cell_value: int) -> Cell:
        """Convert a raw value from the generator into a cell.

        Args:
            cell_value: The integer describing a cell, as returned by
                the maze generator.

        Returns:
            The matching ``Cell`` object.
        """
        return Cell(cell_value)

    def generate_maze(self) -> list[list[Cell]]:
        """Generate a maze and convert it into a grid of cells.

        Returns:
            A list of rows, where each row is a list of ``Cell``
            objects.
        """
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
