from enum import Enum
from random import shuffle

import pygame
from pygame import Surface

from src.maze.maze import Maze


class PacgumType(Enum):
    """The two kinds of gums the player can eat.

    Attributes:
        NORMAL: A small pacgum.
        SUPER: A super-pacgum that makes ghosts edible.
    """

    NORMAL = 1
    SUPER = 2


class Pacgum:
    """Place and draw the pacgums and super-pacgums of a maze.

    Super-pacgums are put in the four corners of the maze. Normal
    pacgums are put on randomly chosen cells, except on the corners and
    on the cells of the "42" pattern.

    Attributes:
        maze: The maze that holds the cells.
        super_gum_positions: The (row, column) cells of the four
            corners, where the super-pacgums are placed.
        cell_positions: The (row, column) cells still available for
            normal pacgums.
        pacgum_number: How many normal pacgums are placed.
        pacgum_counter: Counter initialised with the number of normal
            pacgums.
        pac_gum_positions: The (row, column) cells that received a
            normal pacgum.
        super_pacgum_duration: How long ghosts stay edible, in seconds.
    """

    def __init__(
        self,
        maze: Maze,
        super_pacgum_duration: int = 10,
    ) -> None:
        """Create the gums and place them in the maze.

        Args:
            maze: The maze in which the gums are placed.
            super_pacgum_duration: How long ghosts stay edible after a
                super-pacgum is eaten, in seconds.
        """
        self.maze = maze
        self.super_gum_positions = (
            (0, 0),
            (self.maze.config.height - 1, 0),
            (0, self.maze.config.width - 1),
            (self.maze.config.height - 1, self.maze.config.width - 1),
        )
        self.cell_positions = self.__get_allowed_positions()
        self.pacgum_number = int(
            (self.maze.config.width * self.maze.config.height) * 0.50
        )
        self.pacgum_counter = self.pacgum_number
        self.pac_gum_positions = self.__put_gums()
        self.super_pacgum_duration = super_pacgum_duration

    def __get_allowed_positions(self) -> list[tuple[int, int]]:
        """List the cells where a normal pacgum can be placed.

        A cell is allowed if it is not part of the "42" pattern and is
        not one of the super-pacgum corners.

        Returns:
            The allowed (row, column) positions.
        """
        positions: list[tuple[int, int]] = []
        for y in range(self.maze.config.height):
            for x in range(self.maze.config.width):
                cell = self.maze.grid[y][x]
                if not cell.is_42 and (y, x) not in self.super_gum_positions:
                    positions.append((y, x))
        return positions

    def draw(self, screen: Surface) -> None:
        """Draw the remaining pacgums and super-pacgums on the screen.

        Only the cells that still contain a gum are drawn.

        Args:
            screen: The surface to draw on.
        """
        gum = pygame.image.load("assets/images/gum.png").convert_alpha()
        super_gum = pygame.image.load(
            "assets/images/super_gum.png"
        ).convert_alpha()
        for y, x in self.pac_gum_positions:
            cell = self.maze.grid[y][x]
            if cell.has_pacgum:
                screen.blit(gum, cell.content_position_px)

        for y, x in self.super_gum_positions:
            cell = self.maze.grid[y][x]
            if cell.has_super_pacgum:
                screen.blit(super_gum, cell.content_position_px)

    def __put_gums(self) -> list[tuple[int, int]]:
        """Place the normal pacgums and the super-pacgums in the maze.

        Normal pacgums are put on random allowed cells, and each chosen
        cell is removed from the available positions. Super-pacgums are
        then put on the four corners.

        Returns:
            The (row, column) positions of the normal pacgums.
        """
        positions: list[tuple[int, int]] = []
        for _ in range(self.pacgum_number):
            shuffle(self.cell_positions)
            y, x = self.cell_positions.pop(0)
            positions.append((y, x))
            self.maze.grid[y][x].has_pacgum = True
        for y, x in self.super_gum_positions:
            self.maze.grid[y][x].has_super_pacgum = True
        return positions
