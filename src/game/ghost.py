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
        self.position: tuple[int, int] | None = None
        self.spawn_position: tuple[int, int] | None = None
        self.set_position(position)
        self.direction = Direction.NORTH
        self.behavior = GhostBehavior.CHASE
        self.color = color
        self.position_px = (0, 0)
        self.target: tuple[int, int] | None = None
        self.progress = 0
        self.speed = 2

    def set_position(self, position: tuple[int, int]) -> None:
        self.position = position
        self.spawn_position = position

    @property
    def is_edible(self) -> bool:
        """Whether the player can currently eat this ghost."""
        return self.behavior == GhostBehavior.FLEE

    def move(self, state: GameState) -> None:
        """Advance one step according to the current behavior mode."""
        if self.target is not None:
            return

        options = self._valid_directions(state.maze)
        self.direction = self._choose_direction(state, options)

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

    def respawn(self) -> None:
        self.position = self.spawn_position
        self.target = None

    def _valid_directions(self, maze: Maze) -> list[Direction]:
        """Directions not blocked by a wall, excluding reversal unless
        it's the only option (dead end)."""
        directions = list(Direction)
        random.shuffle(directions)
        col, row = self.position

        options = [d for d in directions if maze.can_move(col, row, d)]

        return options

    def _choose_direction(
        self, state: GameState, options: list[Direction]
    ) -> Direction:
        """PLACEHOLDER for step 2: random choice among valid options.
        Once this is confirmed working, this is the only method that
        changes to add real chase targeting (compare each option's
        resulting distance to player_position, pick the minimum).
        """
        player_row, player_col = state.player.current_cell
        player_position = player_col, player_row

        ghost_col, ghost_row = self.position
        distances: list[tuple[int, Direction]] = []

        for option in options:
            dx, dy = _DELTA[option]
            neighbor = ghost_col + dx, ghost_row + dy

            distance = state.maze.distance(neighbor, player_position)
            if distance is not None:
                distances.append((distance, option))

        if not distances:
            return random.choice(options)

        if self.behavior == GhostBehavior.CHASE:
            return min(distances, key=lambda item: item[0])[1]
        elif self.behavior == GhostBehavior.FLEE:
            return max(distances, key=lambda item: item[0])[1]

        return random.choice(options)

    def draw(
        self, screen: Surface, state: GameState, animation_time: float
    ) -> None:
        sheet = pygame.image.load(
            f"assets/images/ghosts/{self.color.value}_ghost.png"
        ).convert_alpha()

        scared_ghost_themes = [
            "assets/images/ghosts/scared_white_ghost.png",
            "assets/images/ghosts/scared_dark_ghost.png",
        ]

        count = len(scared_ghost_themes)
        scared_frame = (int(animation_time // 0.500)) % count
        normal_frame = (int(animation_time // 0.150)) % 4

        if self.behavior == GhostBehavior.FLEE:
            sheet = pygame.image.load(
                scared_ghost_themes[scared_frame]
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
        self.position_px = (screen_x, screen_y)

        frame_width = 32
        frame_height = 32

        sprite = sheet.subsurface(
            (normal_frame * frame_width, 0, frame_width, frame_height)
        )
        screen.blit(sprite, (screen_x, screen_y))
