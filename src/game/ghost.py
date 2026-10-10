from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.state import GameState

import random
from enum import Enum, auto

import pygame
from pygame import Surface

from src.config.paths import resource_path
from src.game.direction import Direction
from src.maze.cell import Cell

_DELTA = {
    Direction.NORTH: (0, -1),
    Direction.SOUTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
}

_OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}


class GhostBehavior(Enum):
    """The behavior mode a ghost can be in.

    Attributes:
        CHASE: The ghost pursues the player.
        FLEE: The ghost is edible and runs away from the player.
        EATEN: The ghost was eaten and is returning to its spawn.
    """

    CHASE = auto()  # actively pursuing the player
    FLEE = auto()  # edible/frightened, running from the player
    EATEN = auto()  # caught by the player, returning to spawn


class GhostColor(Enum):
    """The color of a ghost, which also selects its sprite sheet.

    Attributes:
        RED: Red ghost.
        PINK: Pink ghost.
        BLUE: Blue ghost.
        ORANGE: Orange ghost.
    """

    RED = "red"
    PINK = "pink"
    BLUE = "blue"
    ORANGE = "orange"


_RANDOM_MOVEMENT_GHOSTS_BY_LEVEL: dict[int, frozenset[GhostColor]] = {
    5: frozenset({GhostColor.BLUE, GhostColor.ORANGE, GhostColor.PINK}),
    6: frozenset({GhostColor.BLUE, GhostColor.PINK}),
    7: frozenset({GhostColor.PINK}),
}


class Ghost:
    """A ghost that moves through the maze, randomly or by distance.

    Depending on the level and on its color, a ghost either moves
    randomly or uses the maze distance to chase or flee the player.

    Attributes:
        position: Current (column, row) cell of the ghost.
        spawn_position: Cell where the ghost starts and respawns.
        direction: Direction of the last chosen move.
        behavior: Current behavior mode of the ghost.
        color: Color of the ghost, used to pick its sprite.
        position_px: Last screen position (x, y) where it was drawn.
        target: Cell the ghost is moving toward, or None if idle.
        progress: Movement progress toward the target cell.
        speed: Progress added to the movement on each update.
    """

    def __init__(self, position: tuple[int, int], color: GhostColor) -> None:
        """Create a ghost at a given cell.

        Args:
            position: The (column, row) cell where the ghost spawns.
            color: The color of the ghost.
        """
        self.position: tuple[int, int] = position
        self.spawn_position: tuple[int, int] = position
        self.set_position(position)
        self.direction = Direction.NORTH
        self.behavior = GhostBehavior.CHASE
        self.color = color
        self.position_px = (0.0, 0.0)
        self.target: tuple[int, int] | None = None
        self.progress = 0
        self.speed = 2
        self.delay_time = 0.0

    def set_position(self, position: tuple[int, int]) -> None:
        """Place the ghost on a cell and set it as its spawn cell.

        Args:
            position: The (column, row) cell to place the ghost on.
        """
        self.position_px = (0.0, 0.0)
        self.position = position
        self.spawn_position = position

    @property
    def is_edible(self) -> bool:
        """Tell whether the player can currently eat this ghost.

        Returns:
            True if the ghost is in the FLEE behavior, False otherwise.
        """
        return self.behavior == GhostBehavior.FLEE

    def move(self, state: GameState) -> None:
        """Start a move to a neighboring cell if the ghost is idle.

        Does nothing while the ghost is still moving toward a target.
        Otherwise it picks a direction among the valid ones, according
        to the current level, and sets the next target cell.

        Args:
            state: The current game state.
        """
        if self.target is not None or self.delay_time > 0:
            return

        uses_random_movement = self._uses_random_movement(state.level)

        options = self._valid_directions(state, uses_random_movement)
        self.direction = self._choose_direction(
            state, options, uses_random_movement
        )

        dx, dy = _DELTA[self.direction]
        col, row = self.position
        self.target = col + dx, row + dy
        self.progress = 0

    def update_position(self) -> None:
        """Advance the movement toward the target cell.

        Adds the ghost speed to the progress. When the progress reaches
        a full cell, the ghost arrives on the target cell and becomes
        idle again.
        """
        if self.target is None:
            return

        self.progress += self.speed
        if self.progress >= Cell.CELL_SIZE * 2:
            self.position = self.target
            self.target = None
            self.progress = 0

    def set_behavior(self, behavior: GhostBehavior) -> None:
        """Change the behavior mode of the ghost.

        Args:
            behavior: The new behavior mode, for example FLEE after
                the player eats a super-pacgum.
        """
        self.behavior = behavior

    def respawn(self) -> None:
        """Send the ghost back to its spawn cell and cancel its move."""
        self.behavior = GhostBehavior.CHASE
        self.position = self.spawn_position
        self.position_px = (0.0, 0.0)
        self.target = None

    def _uses_random_movement(self, level: int) -> bool:
        """Tell whether this ghost moves randomly on a given level.

        All ghosts move randomly before level 5. From level 5, only
        the colors listed for that level do, and from level 8 none of
        them do.

        Args:
            level: The current level number.

        Returns:
            True if the ghost moves randomly, False if it uses the
            distance to the player.
        """
        return level < 5 or self.color in _RANDOM_MOVEMENT_GHOSTS_BY_LEVEL.get(
            level, frozenset()
        )

    def _valid_directions(
        self, state: GameState, uses_random_movement: bool
    ) -> list[Direction]:
        """List the directions the ghost can take from its cell.

        Directions are shuffled, then the ones blocked by a wall are
        removed. A ghost with random movement also avoids going back
        the way it came, unless that is its only option.

        Args:
            state: The current game state, used to check for walls.
            uses_random_movement: Whether the ghost moves randomly.

        Returns:
            The directions that can be taken, in random order.
        """
        directions = list(Direction)
        random.shuffle(directions)
        col, row = self.position

        options = [d for d in directions if state.maze.can_move(col, row, d)]

        non_reverse = []
        if uses_random_movement:
            non_reverse = [
                d for d in options if d != _OPPOSITE[self.direction]
            ]

        return non_reverse or options

    def _choose_direction(
        self,
        state: GameState,
        options: list[Direction],
        uses_random_movement: bool,
    ) -> Direction:
        """Choose the next direction for the ghost.

        A ghost with random movement picks any option at random.
        Otherwise, for each option, the maze distance from the
        neighbor cell to the player is computed. A chasing ghost takes
        the smallest distance and a fleeing ghost takes the largest. A
        random option is used if no distance is available or for any
        other behavior.

        Args:
            state: The current game state.
            options: The valid directions to choose from.
            uses_random_movement: Whether the ghost moves randomly.

        Returns:
            The chosen direction.
        """
        if uses_random_movement:
            return random.choice(options)

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
        """Draw the ghost on the screen.

        Picks the sprite sheet from the ghost color, or a scared sheet
        when it is fleeing, then selects the animation frame from the
        elapsed time. While moving, the position is interpolated
        between the current cell and the target cell.

        Args:
            screen: The surface to draw on.
            state: The current game state, used for the maze offsets.
            animation_time: Elapsed time in seconds, used to choose the
                animation frame.
        """
        sheet = pygame.image.load(
            resource_path(f"assets/images/ghosts/{self.color.value}_ghost.png")
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
                resource_path(scared_ghost_themes[scared_frame])
            ).convert_alpha()

        col, row = float(self.position[0]), float(self.position[1])
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

        sprite_area = normal_frame * frame_width, 0, frame_width, frame_height
        screen.blit(sheet, (screen_x, screen_y), sprite_area)
