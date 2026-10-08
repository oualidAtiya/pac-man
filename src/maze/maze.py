from collections import deque

import pygame
from pygame import Surface
from src.maze.generator_error import GeneratorError
from src.config.models import GameConfig
from src.game.direction import Direction
from src.maze.adapter import MazeAdapter


class Maze:
    """The maze of a level: its cells, size, screen layout and drawing.

    It builds the grid through the maze adapter, computes where the
    maze is placed on the screen, answers movement and distance
    questions, and draws the walls.

    Attributes:
        grid: The cells of the maze, indexed as ``grid[row][column]``.
        config: The game configuration, whose width and height change
            from one level to the next.
        default: The initial (height, width) of the maze, used to go
            back to the first level size.
        width_maze_px: Width of the maze in pixels.
        height_maze_px: Height of the maze in pixels.
        offest_x: Horizontal pixel offset where the maze is drawn.
        offest_y: Vertical pixel offset where the maze is drawn.
    """

    def __init__(self, config: GameConfig) -> None:
        """Generate the maze and compute its screen layout.

        Args:
            config: The game configuration, used for the maze size
                and seed.

        Raises:
            GeneratorError: If the maze generation fails.
        """
        try:
            self.grid = MazeAdapter(config).generate_maze()
        except Exception:
            raise GeneratorError("Maze Generation Failed")
        self.config = config
        self.default = config.height, config.width
        self.width_maze_px = 0
        self.height_maze_px = 0
        self.offest_x = 0
        self.offest_y = 0
        self.set_height_width_px()
        self.set_offests()
        self.set_cells_positions()

    def set_height_width_px(self) -> None:
        """Compute the size of the maze in pixels from its cell count."""
        self.width_maze_px = (32 * self.config.width + 1) + (
            32 * self.config.width
        )
        self.height_maze_px = (32 * self.config.height + 1) + (
            32 * self.config.height
        )

    def set_offests(self) -> None:
        """Compute the pixel offsets that center the maze on screen."""
        self.offest_x = (2000 // 2) - (self.config.width * 32)
        self.offest_y = (1500 // 2) - (self.config.height * 32)

    def can_move(self, col: int, row: int, direction: Direction) -> bool:
        """Check whether a move from a cell in a direction is possible.

        The move is possible if it stays inside the maze and no wall
        blocks it.

        Args:
            col: The column of the starting cell.
            row: The row of the starting cell.
            direction: The direction to test.

        Returns:
            True if the move is allowed, False otherwise.
        """
        if direction == Direction.NORTH:
            return row - 1 >= 0 and not self.grid[row][col].north

        if direction == Direction.SOUTH:
            return (
                row + 1 < self.config.height and not self.grid[row][col].south
            )

        if direction == Direction.WEST:
            return col - 1 >= 0 and not self.grid[row][col].west

        if direction == Direction.EAST:
            return col + 1 < self.config.width and not self.grid[row][col].east

    def distance(
        self,
        first_position: tuple[int, int],
        second_position: tuple[int, int],
    ) -> int | None:
        """Compute the shortest path length between two cells.

        Uses a breadth-first search that only follows open passages.

        Args:
            first_position: The (column, row) of the starting cell.
            second_position: The (column, row) of the target cell.

        Returns:
            The number of steps of the shortest path, or None if the
            target cannot be reached.
        """
        queue = deque([(first_position, 0)])
        visited = {first_position}

        while queue:
            (col, row), curr_distance = queue.popleft()

            if (col, row) == second_position:
                return curr_distance

            for direction in Direction:
                if not self.can_move(col, row, direction):
                    continue

                if direction == Direction.NORTH:
                    next_position = col, row - 1
                elif direction == Direction.SOUTH:
                    next_position = col, row + 1
                elif direction == Direction.WEST:
                    next_position = col - 1, row
                elif direction == direction.EAST:
                    next_position = col + 1, row

                if next_position in visited:
                    continue

                next_distance = curr_distance + 1

                visited.add(next_position)
                queue.append((next_position, next_distance))

        return None

    def regenerate_maze(self, next_level: bool) -> None:
        """Generate a new maze and update its screen layout.

        For the next level, the width and height each grow by one.
        Otherwise they go back to their initial values.

        Args:
            next_level: True to build a bigger maze for the next
                level, False to go back to the first level size.

        Raises:
            GeneratorError: If the maze generation fails.
        """
        if next_level:
            self.config.width += 1
            self.config.height += 1
        else:
            self.config.height = self.default[0]
            self.config.width = self.default[1]
        try:
            self.grid = MazeAdapter(self.config).generate_maze()
        except Exception:
            raise GeneratorError("Maze Generation Failed")
        self.set_height_width_px()
        self.set_offests()
        self.set_cells_positions()

    def set_cells_positions(self) -> None:
        """Set the pixel position of the content of every cell."""
        x_px = self.offest_x
        y_px = self.offest_y
        for y in range(self.config.height):
            for x in range(self.config.width):
                cell = self.grid[y][x]
                cell.content_position_px = (x_px + 32, y_px + 32)
                x_px += 32 * 2
            y_px += 32 * 2
            x_px = self.offest_x

    def draw(self, screen: Surface) -> None:
        """Draw the walls of the whole maze on the screen.

        For each cell, the four corner images are chosen from the
        walls of the cell and of its neighbors, then the wall segments
        between the corners are drawn for each closed side.

        Args:
            screen: The surface to draw on.
        """
        corners = {
            i: pygame.image.load(
                f"assets/images/corners/{i}x32.png"
            ).convert_alpha()
            for i in range(1, 17)
        }
        cell_width = 32

        x_px = self.offest_x
        y_px = self.offest_y

        for y in range(self.config.height):
            for x in range(self.config.width):
                cell = self.grid[y][x]
                west_cell = None
                north_cell = None
                east_cell = None
                south_cell = None
                if x > 0:
                    west_cell = self.grid[y][x - 1]
                if y > 0:
                    north_cell = self.grid[y - 1][x]
                if x < self.config.width - 1:
                    east_cell = self.grid[y][x + 1]
                if y < self.config.height - 1:
                    south_cell = self.grid[y + 1][x]

                screen.blit(
                    corners[cell.get_nw_corner(north_cell, west_cell)],
                    (x_px, y_px),
                )
                screen.blit(
                    corners[cell.get_ne_corner(north_cell, east_cell)],
                    (x_px + cell_width * 2, y_px),
                )
                screen.blit(
                    corners[cell.get_se_corner(east_cell, south_cell)],
                    (x_px + cell_width * 2, y_px + cell_width * 2),
                )
                screen.blit(
                    corners[cell.get_sw_corner(west_cell, south_cell)],
                    (x_px, y_px + cell_width * 2),
                )
                if cell.north:
                    screen.blit(corners[6], (x_px + cell_width, y_px))
                if cell.south:
                    screen.blit(
                        corners[6], (x_px + cell_width, y_px + cell_width * 2)
                    )
                if cell.east:
                    screen.blit(
                        corners[5], (x_px + cell_width * 2, y_px + cell_width)
                    )
                if cell.west:
                    screen.blit(corners[5], (x_px, y_px + cell_width))
                x_px += cell_width * 2
            y_px += cell_width * 2
            x_px = self.offest_x
