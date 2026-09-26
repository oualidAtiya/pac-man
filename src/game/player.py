from src.maze.maze import Maze
import pygame
from pygame import Surface
from src.game.direction import Direction


class Player:

    def __init__(self, maze: Maze) -> None:
        self.height = maze.config.height
        self.width = maze.config.width
        self.maze = maze
        self.current_cell = (self.width//2, self.height//2)
        self.position = ((maze.width_maze_px//2)+maze.offest_x, (maze.height_maze_px//2)+maze.offest_y)
        self.current_direction = Direction.EAST

    def draw(self, screen: Surface) -> None:
        x_px, y_px = self.position
        if self.current_direction == Direction.SOUTH:
            screen.blit(pygame.image.load(f"assets/images/pac-man.png").convert_alpha(), (x_px, y_px))
        elif self.current_direction == Direction.EAST:
            screen.blit(pygame.image.load(f"assets/images/pac-man.png").convert_alpha(), (x_px, y_px))
        elif self.current_direction == Direction.NORTH:
            screen.blit(pygame.image.load(f"assets/images/pac-man.png").convert_alpha(), (x_px, y_px))
        else:
            screen.blit(pygame.image.load(f"assets/images/pac-man.png").convert_alpha(), (x_px, y_px))

    def try_move(self, direction: Direction) -> bool | tuple[int, int]:
        y, x = self.current_cell
        if direction == Direction.SOUTH:
            if 0 <= y+1 <= self.height -1 and not self.maze.grid[y][x].south:
                self.position = (self.position[0], self.position[1]+64)
                self.current_direction = direction
                self.current_cell = (y+1, x)
                return (y+1, x)
            return False
        elif direction == Direction.NORTH:
            if 0 <= y-1 <= self.height -1 and not self.maze.grid[y][x].north:
                self.position = (self.position[0], self.position[1]-64)
                self.current_direction = direction
                self.current_cell = (y-1, x)
                return (y-1, x)
            return False
        elif direction == Direction.EAST:
            if 0 <= x+1 <= self.width -1 and not self.maze.grid[y][x].east:
                self.position = (self.position[0]+64, self.position[1])
                self.current_direction = direction
                self.current_cell = (y, x+1)
                return (y, x+1)
            return False
        elif direction == Direction.WEST:
            if 0 <= x+1 <= self.width -1 and not self.maze.grid[y][x].west:
                self.position = (self.position[0]-64, self.position[1])
                self.current_direction = direction
                self.current_cell = (y, x-1)
                return (y, x-1)
            return False
