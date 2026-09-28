from __future__ import annotations

import random
from enum import Enum, auto

import pygame
from pygame import Surface

from src.game.direction import Direction
from src.maze.cell import Cell
from src.maze.maze import Maze

_OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

_DELTA = {
    Direction.NORTH: (0, -1),
    Direction.SOUTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
}


class GhostBehavior(Enum):
    """A ghost's current behavioral mode."""

    CHASE = auto()  # actively pursuing the player
    FLEE = auto()  # edible/frightened, running from the player
    EATEN = auto()  # caught by the player, returning to spawn


class GhostColor(Enum):
    RED = "red"
    PINK = "pink"
    BLUE = "blue"
    ORANGE = "orange"


class Ghost:
    """A single ghost entity."""

    def __init__(self, position: tuple[int, int], color: GhostColor) -> None:
        self.position = position  # (col, row)
        self.spawn_position = position
        self.direction = Direction.NORTH
        self.behavior = GhostBehavior.CHASE
        self.color = color  # identifies which corner it spawned in

    @property
    def is_edible(self) -> bool:
        """Whether the player can currently eat this ghost."""
        return self.behavior == GhostBehavior.FLEE

    def move(self, maze: Maze, player_position: tuple[int, int]) -> None:
        """Advance one step according to the current behavior mode."""
        options = self._valid_directions(maze)
        self.direction = self._choose_direction(options, player_position)

    def update_position(self) -> None:
        dx, dy = _DELTA[self.direction]
        col, row = self.position
        self.position = col + dx, row + dy

    def set_behavior(self, behavior: GhostBehavior) -> None:
        """Transition to a new behavior mode (e.g. on super-pacgum pickup)."""
        self.behavior = behavior

    def _valid_directions(self, maze: Maze) -> list[Direction]:
        """Directions not blocked by a wall, excluding reversal unless
        it's the only option (dead end)."""
        directions = list(Direction)
        random.shuffle(directions)
        col, row = self.position

        options = [d for d in directions if maze.can_move(col, row, d)]
        non_reverse = [d for d in options if d != _OPPOSITE[self.direction]]
        return non_reverse or options

    def _choose_direction(
        self, options: list[Direction], player_position: tuple[int, int]
    ) -> Direction:
        """PLACEHOLDER for step 2: random choice among valid options.
        Once this is confirmed working, this is the only method that
        changes to add real chase targeting (compare each option's
        resulting distance to player_position, pick the minimum).
        """
        return random.choice(options)

    def draw(self, screen: Surface, maze: Maze) -> None:
        sheet = pygame.image.load(
            f"assets/images/ghosts/{self.color.value}_ghost.png"
        ).convert_alpha()
        start_x = maze.offest_x + Cell.CELL_SIZE
        start_y = maze.offest_y + Cell.CELL_SIZE

        screen_x = start_x + self.position[0] * Cell.CELL_SIZE * 2
        screen_y = start_y + self.position[1] * Cell.CELL_SIZE * 2

        sprite = sheet.subsurface((0, 0, 32, 32))
        screen.blit(sprite, (screen_x, screen_y))
