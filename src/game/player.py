import pygame
from pygame import Surface

from src.game.direction import Direction
from src.game.pacgum import PacgumType
from src.game.state import GameState
from src.maze.maze import Maze
from src.config.paths import resource_path


class Player:
    """The player-controlled Pac-Man.

    Handles movement from cell to cell, animation frames, eating gums,
    lives and score.

    Attributes:
        maze: The maze the player moves in.
        start_cell: The (row, column) cell where the player starts.
        current_cell: The (row, column) cell the player is on.
        position: The (x, y) screen position of the player in pixels.
        respawn_position: The pixel position used after losing a life.
        current_direction: Direction of the current move, or None.
        dead_position: The pixel position where the death animation
            is drawn.
        next_direction: Direction requested by the player, used as
            soon as the current move ends.
        target: The cell the player is moving toward, or None.
        score: The current score.
        dead_counter: Counter driving the death animation.
        lives: Number of remaining lives.
        acc: Pixels moved so far toward the target cell.
    """

    def __init__(self, maze: Maze) -> None:
        """Create the player and place it at the start cell.

        Args:
            maze: The maze the player moves in.
        """
        self.maze = maze
        self.start_cell = (0, 0)
        self.current_cell = (0, 0)
        self.position = (0, 0)
        self.respawn_position = (0, 0)
        self.current_direction: Direction | None = None
        self.dead_position = (0, 0)
        self.next_direction: Direction | None = None
        self.target: tuple[int, int] | None = None
        self.score = 0
        self.dead_counter = 0
        self.lives = maze.config.lives
        self.acc = 0
        self.set_attr()

    def set_attr(self) -> None:
        """Set the start cell and pixel position from the maze size.

        The start cell is the middle of the maze. When the height is
        even, the column is shifted one cell to the left.
        """
        if self.maze.config.height % 2 == 0:
            self.start_cell = (
                self.maze.config.height // 2,
                self.maze.config.width // 2 - 1,
            )
        else:
            self.start_cell = (
                self.maze.config.height // 2,
                self.maze.config.width // 2,
            )
        self.current_cell = self.start_cell
        self.position = self.maze.grid[self.start_cell[0]][
            self.start_cell[1]
        ].content_position_px
        self.respawn_position = self.position
        self.dead_counter = 0

    def is_time_out(self, state: GameState) -> bool:
        """Tell whether the level time is over.

        Args:
            state: The current game state.

        Returns:
            True if no time remains, False otherwise.
        """
        return state.time_remaining == 0

    def is_win(self, state: GameState) -> bool:
        """Tell whether the player has won the game.

        The game is won when all pacgums are eaten on the last level
        (level 10) with time still remaining.

        Args:
            state: The current game state.

        Returns:
            True if the winning conditions are met, False otherwise.
        """
        return (
            state.pacgum.pacgum_counter == 0
            and state.level == 10
            and state.time_remaining > 0
        )

    def _get_current_frame(self, alive: bool) -> int:
        """Get the animation frame index to display.

        When alive, the frame depends on the pixels moved (``acc``).
        When dead, it depends on the death counter.

        Args:
            alive: True for the walking animation, False for the death
                animation.

        Returns:
            The index of the frame to use.
        """
        if alive:
            if 0 <= self.acc <= 16:
                return 0
            if 32 < self.acc <= 48:
                return 2
            return 1
        else:
            if 90 <= self.dead_counter <= 120:
                return 0
            if 60 <= self.dead_counter < 90:
                return 1
            if 30 <= self.dead_counter < 60:
                return 2
            return 3

    def draw_die_state(self, screen: Surface) -> None:
        """Draw the current frame of the death animation.

        Args:
            screen: The surface to draw on.
        """
        path = "assets/images/pac-man"
        frames = ["1.png", "2.png", "3.png", "4.png"]
        current_frame = self._get_current_frame(False)
        screen.blit(
            pygame.image.load(
                resource_path(f"{path}_dead/{frames[current_frame]}")
            ).convert_alpha(),
            (self.dead_position),
        )

    def draw(self, screen: Surface) -> None:
        """Draw the player on the screen.

        Draws the death animation if the player is dying. Otherwise it
        draws the walking frame that matches the current direction.

        Args:
            screen: The surface to draw on.
        """
        path = "assets/images/pac-man"
        if self.dead_counter > 0:
            self.draw_die_state(screen)
            return

        frames = ["1.png", "2.png", "3.png"]
        x_px, y_px = self.position
        current_frame = self._get_current_frame(True)
        if self.current_direction == Direction.SOUTH:
            screen.blit(
                pygame.image.load(
                   resource_path(f"{path}_down/{frames[current_frame]}")
                ).convert_alpha(),
                (x_px, y_px),
            )
        elif self.current_direction == Direction.EAST:
            screen.blit(
                pygame.image.load(
                    resource_path(f"{path}_right/{frames[current_frame]}")
                ).convert_alpha(),
                (x_px, y_px),
            )
        elif self.current_direction == Direction.NORTH:
            screen.blit(
                pygame.image.load(
                    resource_path(f"{path}_up/{frames[current_frame]}")
                ).convert_alpha(),
                (x_px, y_px),
            )
        else:
            screen.blit(
                pygame.image.load(
                   resource_path(f"{path}_left/{frames[current_frame]}")
                ).convert_alpha(),
                (x_px, y_px),
            )

    def update_position(self) -> bool:
        """Move the player a few pixels toward its target cell.

        When the full cell distance is reached, the player arrives on
        the target cell. It then continues with the requested
        direction if possible, else with the current direction, else
        it stops.

        Returns:
            True if the player arrived on a new cell during this call,
            False otherwise.
        """
        step = 4
        if self.target:
            if self.current_direction == Direction.SOUTH:
                self.position = (self.position[0], self.position[1] + step)
            elif self.current_direction == Direction.NORTH:
                self.position = (self.position[0], self.position[1] - step)
            elif self.current_direction == Direction.WEST:
                self.position = (self.position[0] - step, self.position[1])
            else:
                self.position = (self.position[0] + step, self.position[1])
            self.acc += step
            if self.acc == 64:
                self.current_cell = self.target
                self.target = None
                self.acc = 0
                if self.next_direction and self._can_move(self.next_direction):
                    self.request_move(self.next_direction)
                elif self.current_direction and self._can_move(
                    self.current_direction
                ):
                    self.request_move(self.current_direction)
                else:
                    self.next_direction = None
                return True
        return False

    def _can_move(self, direction: Direction) -> tuple[int, int] | None:
        """Check whether the player can move one cell in a direction.

        The move is allowed if the next cell is inside the maze and no
        wall blocks the way from the current cell.

        Args:
            direction: The direction to test.

        Returns:
            The (row, column) of the next cell if the move is possible,
            None otherwise.
        """
        y, x = self.current_cell
        if direction == Direction.SOUTH:
            if (
                0 <= y + 1 <= self.maze.config.height - 1
                and not self.maze.grid[y][x].south
            ):
                return (y + 1, x)
            return None
        elif direction == Direction.NORTH:
            if (
                0 <= y - 1 <= self.maze.config.height - 1
                and not self.maze.grid[y][x].north
            ):
                return (y - 1, x)
            return None
        elif direction == Direction.EAST:
            if (
                0 <= x + 1 <= self.maze.config.width - 1
                and not self.maze.grid[y][x].east
            ):
                return (y, x + 1)
            return None
        elif direction == Direction.WEST:
            if (
                0 <= x - 1 <= self.maze.config.width - 1
                and not self.maze.grid[y][x].west
            ):
                return (y, x - 1)
            return None

    def request_move(self, direction: Direction) -> None:
        """Ask the player to move in a direction.

        If the player is idle and the move is possible, it starts at
        once. Otherwise the direction is stored and used later.

        Args:
            direction: The requested direction.
        """
        if not self.target and self._can_move(direction):
            self.target = self._can_move(direction)
            self.current_direction = direction
        else:
            self.next_direction = direction

    def eat_current_cell(self) -> None | PacgumType:
        """Eat the gum on the current cell, if there is one.

        A super-pacgum has priority over a normal pacgum. The eaten
        gum is removed from the cell.

        Returns:
            The type of gum eaten, or None if the cell had no gum.
        """
        y, x = self.current_cell
        cell = self.maze.grid[y][x]
        if cell.has_super_pacgum:
            cell.has_super_pacgum = False
            return PacgumType.SUPER
        if cell.has_pacgum:
            cell.has_pacgum = False
            return PacgumType.NORMAL
        return None

    def respawn(self) -> None:
        """Put the player back on its start cell and reset its move."""
        self.current_cell = self.start_cell
        self.position = self.respawn_position
        self.acc = 0
        self.target = None
        self.current_direction = None
        self.next_direction = None

    def lose_life(self) -> bool:
        """Remove one life from the player.

        Returns:
            True if the player has no lives left, False otherwise.
        """
        self.lives -= 1
        return self.lives == 0

    def add_score(self, score: int) -> None:
        """Add points to the score.

        Args:
            score: The number of points to add.
        """
        self.score += score
