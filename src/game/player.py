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
        self.target = None
        self.acc = 0


    def get_current_frame(self):
        if  0 <= self.acc <= 16:
            return 0
        if  16 < self.acc <= 32:
            return 1
        if  32 < self.acc <= 48:
            return 2
        else:
            return 1

    def draw(self, screen: Surface) -> None:
        x_px, y_px = self.position
        frames = ["1.png", "2.png", "3.png"]
        current_frame = self.get_current_frame()
        if self.current_direction == Direction.SOUTH:
            screen.blit(pygame.image.load(f"assets/images/pac-man_down/{frames[current_frame]}").convert_alpha(), (x_px, y_px))
        elif self.current_direction == Direction.EAST:
            screen.blit(pygame.image.load(f"assets/images/pac-man_right/{frames[current_frame]}").convert_alpha(), (x_px, y_px))
        elif self.current_direction == Direction.NORTH:
            screen.blit(pygame.image.load(f"assets/images/pac-man_up/{frames[current_frame]}").convert_alpha(), (x_px, y_px))
        else:
            screen.blit(pygame.image.load(f"assets/images/pac-man_left/{frames[current_frame]}").convert_alpha(), (x_px, y_px))


    def update_position(self) -> bool:
        step = 4
        if self.target:
            if (self.current_direction == Direction.SOUTH):
                self.position = (self.position[0], self.position[1]+step)
            elif (self.current_direction == Direction.NORTH):
                self.position = (self.position[0], self.position[1]-step)
            elif (self.current_direction == Direction.WEST):
                self.position = (self.position[0]-step, self.position[1])
            else:
                self.position = (self.position[0]+step, self.position[1])
            self.acc += step
            if self.acc >= 64:
                self.current_cell = self.target
                self.target = None
                self.acc = 0

    def request_move(self, direction: Direction) -> bool | tuple[int, int]:
        y, x = self.current_cell
        if direction == Direction.SOUTH:
            if 0 <= y+1 <= self.height -1 and not self.maze.grid[y][x].south and not self.target:
                self.current_direction = direction
                self.target = (y+1, x)
                return True
            return False
        elif direction == Direction.NORTH:
            if 0 <= y-1 <= self.height -1 and not self.maze.grid[y][x].north and not self.target:
                self.current_direction = direction
                self.target = (y-1, x)
                return True
            return False
        elif direction == Direction.EAST:
            if 0 <= x+1 <= self.width - 1 and not self.maze.grid[y][x].east and not self.target:
                self.current_direction = direction
                self.target = (y, x+1)
                return True
            return False
        elif direction == Direction.WEST:
            if 0 <= x-1 <= self.width - 1 and not self.maze.grid[y][x].west and not self.target:
                self.current_direction = direction
                self.target = (y, x-1)
                return True
            return False
