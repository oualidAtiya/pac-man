from src.maze.maze import Maze
from pygame import Surface
from random import shuffle
import pygame

class Pacgum:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.super_gum_positions = (
            (0, 0),
            (0, self.maze.height-1),
            (self.maze.width-1, 0),
            (self.maze.width-1, self.maze.height-1)
        )
        self.cell_positions = self.__set_allowed_positions()
        self.pacgum_number = 80
        self.pac_gum_positions = self.__put_gums()

    def __set_allowed_positions(self):
        positions = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]
                if not cell.is_42 and (y, x) not in self.super_gum_positions:
                    positions.append((y, x))
        return positions

 
    def draw(self, screen: Surface) -> None:
        gum = pygame.image.load(
                f"assets/images/gum.png"
            ).convert_alpha()
        super_gum = pygame.image.load(
                f"assets/images/super_gum.png"
            ).convert_alpha()
        for y, x in self.pac_gum_positions:
                cell = self.maze.grid[y][x]
                if (cell.has_pacgum):
                    screen.blit(gum, cell.gum_position)

        for y, x in self.super_gum_positions:
            cell = self.maze.grid[y][x]
            if (cell.has_super_pacgum):
                screen.blit(super_gum, cell.gum_position)
                    
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
