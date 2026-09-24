from src.maze.maze import Maze

from src.game.direction import Direction


class Player:
    """The user-controlled Pac-Man character."""

    def __init__(self, position: tuple[int, int], lives: int) -> None:
        self.position = position  # (col, row)
        self.direction = Direction.WEST  # current facing/movement direction
        self.lives = lives
        self.score = 0

    def move(self, direction: Direction, maze: Maze) -> None:
        """Attempt to move one cell in the given direction, respecting walls."""
        raise NotImplementedError

    def lose_life(self) -> None:
        """Decrement lives after being caught by a non-edible ghost."""
        raise NotImplementedError
