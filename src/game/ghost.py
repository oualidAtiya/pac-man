from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.state import GameState

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

        self.target: tuple[int, int] | None = None
        self.progress = 0
        self.speed = 2

    @property
    def is_edible(self) -> bool:
        """Whether the player can currently eat this ghost."""
        return self.behavior == GhostBehavior.FLEE

    def move(self, state: GameState) -> None:
        """Advance one step according to the current behavior mode."""
        if self.target is not None:
            return

        options = self._valid_directions(state.maze)
        self.direction = self._choose_direction(options, state.player.position)

        dx, dy = _DELTA[self.direction]
        col, row = self.position
        self.target = col + dx, row + dy
        self.progress = 0

    def update_position(self) -> None:
        if self.target is None:
            return

        self.progress += self.speed
        if self.progress >= Cell.CELL_SIZE * 2:
            self.position = self.target
            self.target = None
            self.progress = 0

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
        # TODO: Implement the direction decisions
        # if self.behavior == GhostBehavior.CHASE: ...  # Chase the player
        # elif self.behavior == GhostBehavior.FLEE: ... # Run away from the palyer
        return random.choice(options)

    def draw(self, screen: Surface, state: GameState) -> None:
        sheet = pygame.image.load(
            f"assets/images/ghosts/{self.color.value}_ghost.png"
        ).convert_alpha()

        scared_ghost_themes = [
            "assets/images/ghosts/scared_white_ghost.png",
            "assets/images/ghosts/scared_dark_ghost.png",
        ]

        if self.behavior == GhostBehavior.FLEE:
            count = len(scared_ghost_themes)
            sheet = pygame.image.load(
                scared_ghost_themes[(pygame.time.get_ticks() // 500) % count]
            ).convert_alpha()

        col, row = self.position
        if self.target is not None:
            target_col, target_row = self.target
            ratio = self.progress / (Cell.CELL_SIZE * 2)
            col += (target_col - col) * ratio
            row += (target_row - row) * ratio

        start_x = state.maze.offest_x + Cell.CELL_SIZE
        start_y = state.maze.offest_y + Cell.CELL_SIZE

        screen_x = start_x + col * Cell.CELL_SIZE * 2
        screen_y = start_y + row * Cell.CELL_SIZE * 2

        frame_width = 32
        frame_height = 32

        frame = (pygame.time.get_ticks() // 150) % 4

        sprite = sheet.subsurface(
            (frame * frame_width, 0, frame_width, frame_height)
        )
        screen.blit(sprite, (screen_x, screen_y))
