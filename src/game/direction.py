from enum import Enum, auto


class Direction(Enum):
    """The four cardinal directions used for movement in the maze.

    Each member gets an automatic unique value, so only the member
    names matter when comparing directions.

    Attributes:
        NORTH: Move up.
        EAST: Move right.
        SOUTH: Move down.
        WEST: Move left.
    """

    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
