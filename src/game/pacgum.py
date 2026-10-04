from enum import Enum
from random import shuffle

import pygame
from pygame import Surface

from src.maze.maze import Maze


class PacgumType(Enum):
    NORMAL = 1
    SUPER = 2


class Pacgum:
    def __init__(
        self,
        maze: Maze,
        super_pacgum_duration: int = 10,
    ) -> None:
        self.maze = maze
        self.super_gum_positions = (
            (0, 0),
            (self.maze.config.height - 1, 0),
            (0, self.maze.config.width - 1),
            (self.maze.config.height - 1, self.maze.config.width - 1),
        )
        self.cell_positions = self.__get_allowed_positions()
        self.pacgum_number = int((self.maze.config.width * self.maze.config.height) * 0.50)
        self.pacgum_counter = self.pacgum_number
        self.pac_gum_positions = self.__put_gums()
        self.super_pacgum_duration = super_pacgum_duration

    def __get_allowed_positions(self):
        positions = []
        for y in range(self.maze.config.height):
            for x in range(self.maze.config.width):
                cell = self.maze.grid[y][x]
                if not cell.is_42 and (y, x) not in self.super_gum_positions:
                    positions.append((y, x))
        return positions

    def draw(self, screen: Surface) -> None:
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

    def __put_gums(self) -> None:
        positions = []
        for _ in range(self.pacgum_number):
            shuffle(self.cell_positions)
            y, x = self.cell_positions.pop(0)
            positions.append((y, x))
            self.maze.grid[y][x].has_pacgum = True
        for y, x in self.super_gum_positions:
            self.maze.grid[y][x].has_super_pacgum = True
        return positions
