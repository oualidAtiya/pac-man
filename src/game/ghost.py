from enum import Enum, auto

from src.game.direction import Direction
from src.maze.maze import Maze


class GhostBehavior(Enum):
    """A ghost's current behavioral mode."""

    CHASE = auto()  # actively pursuing the player
    FLEE = auto()  # edible/frightened, running from the player
    EATEN = auto()  # caught by the player, returning to spawn


class Ghost:
    """A single ghost entity."""

    def __init__(self, position: tuple[int, int], color: str) -> None:
        self.position = position  # (col, row)
        self.direction = Direction.NORTH
        self.behavior = GhostBehavior.CHASE
        self.color = color  # identifies which corner it spawned in

    @property
    def is_edible(self) -> bool:
        """Whether the player can currently eat this ghost."""
        return self.behavior == GhostBehavior.FLEE

    def move(self, maze: Maze, player_position: tuple[int, int]) -> None:
        """Advance one step according to the current behavior mode."""
        raise NotImplementedError

    def set_behavior(self, behavior: GhostBehavior) -> None:
        """Transition to a new behavior mode (e.g. on super-pacgum pickup)."""
        self.behavior = behavior
