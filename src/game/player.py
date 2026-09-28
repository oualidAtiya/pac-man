from src.maze.maze import Maze
import pygame
from pygame import Surface
from src.game.direction import Direction


class Player:

    def __init__(self, maze: Maze) -> None:
        self.height = maze.config.height
        self.width = maze.config.width
        self.maze = maze
        self.current_cell = (self.height//2, self.width//2)
        self.position = (
            (maze.width_maze_px//2)+maze.offest_x,
            (maze.height_maze_px//2)+maze.offest_y
        )
        self.current_direction = None
        self.next_direction: None | Direction = None
        self.target: None | tuple[int, int] = None
        self.score = 0
        self.lives = maze.config.lives
        self.acc = 0

    def _get_current_frame(self) -> int:
        if 0 <= self.acc <= 16:
            return 0
        if 16 < self.acc <= 32:
            return 1
        if 32 < self.acc <= 48:
            return 2
        else:
            return 1

    def draw(self, screen: Surface) -> None:
        x_px, y_px = self.position
        frames = ["1.png", "2.png", "3.png"]
        current_frame = self._get_current_frame()
        path = "assets/images/pac-man"
        if self.current_direction == Direction.SOUTH:
            screen.blit(
                pygame.image.load(
                    f"{path}_down/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px))
        elif self.current_direction == Direction.EAST:
            screen.blit(
                pygame.image.load(
                    f"{path}_right/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px)
            )
        elif self.current_direction == Direction.NORTH:
            screen.blit(
                pygame.image.load(
                    f"{path}_up/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px)
            )
        else:
            screen.blit(
                pygame.image.load(
                    f"{path}_left/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px)
            )

    def update_position(self) -> None:
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
            if self.acc == 64:
                self.current_cell = self.target
                self.target = None
                self.acc = 0
                self.eat_current_cell()
                if (self.next_direction
                   and self._can_move(self.next_direction)):
                    self.request_move(self.next_direction)
                elif self.current_direction and self._can_move(self.current_direction):
                    self.request_move(self.current_direction)
                else:
                    self.next_direction = None

    def _can_move(self, direction: Direction) -> tuple[int, int] | None:
        y, x = self.current_cell
        if direction == Direction.SOUTH:
            if 0 <= y+1 <= self.height - 1 and not self.maze.grid[y][x].south:
                return (y+1, x)
            return None
        elif direction == Direction.NORTH:
            if 0 <= y-1 <= self.height - 1 and not self.maze.grid[y][x].north:
                return (y-1, x)
            return None
        elif direction == Direction.EAST:
            if 0 <= x+1 <= self.width - 1 and not self.maze.grid[y][x].east:
                return (y, x+1)
            return None
        elif direction == Direction.WEST:
            if 0 <= x-1 <= self.width - 1 and not self.maze.grid[y][x].west:
                return (y, x-1)
            return None

    def request_move(self, direction: Direction) -> None:
        if (not self.target and self._can_move(direction)):
            self.target = self._can_move(direction)
            self.current_direction = direction
        else:
            self.next_direction = direction

    def eat_current_cell(self) -> None:
        y, x = self.current_cell
        cell = self.maze.grid[y][x]
        if cell.has_super_pacgum:
            cell.has_super_pacgum = False
            self.add_score(self.maze.config.points_per_super_pacgum)
        if cell.has_pacgum:
            cell.has_pacgum = False
            self.add_score(self.maze.config.points_per_pacgum)

    def respawn(self):
        self.current_cell = (self.width//2, self.height//2)
        self.position = (
            (self.maze.width_maze_px//2)+self.maze.offest_x,
            (self.maze.height_maze_px//2)+self.maze.offest_y
        )
        self.current_direction = None
        self.next_direction = None


    def lose_life(self) -> bool:
        self.lives -= 1
        if self.lives == 0:
            return True
        return False

    def add_score(self, score):
        self.score += score
