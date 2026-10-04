import pygame
from pygame import Surface
from src.game.state import GameState
from src.game.direction import Direction
from src.maze.maze import Maze

from src.game.pacgum import PacgumType

class Player:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.start_cell = None
        self.current_cell = None
        self.position = None
        self.respawn_position = None
        self.current_direction = None
        self.dead_position : None | tuple[int, int] = None
        self.next_direction: None | Direction = None
        self.target: None | tuple[int, int] = None
        self.score = 0
        self.dead_counter = 0
        self.lives = maze.config.lives
        self.acc = 0
        self.set_attr()

    def set_attr(self) -> None:
        if (self.maze.config.height % 2 == 0):
            self.start_cell = (self.maze.config.height // 2, self.maze.config.width // 2-1)
        else:
            self.start_cell = (self.maze.config.height // 2, self.maze.config.width // 2)
        self.current_cell = self.start_cell
        self.position = self.maze.grid[self.start_cell[0]][self.start_cell[1]].content_position_px
        self.respawn_position = self.position

    def is_time_out(self, state: GameState) -> bool:
        return state.time_remaining == 0

    def is_win(self, state: GameState) -> bool:
        return (
            state.pacgum.pacgum_counter == 0
            and state.level == 10
            and state.time_remaining > 0
        )

    def _get_current_frame(self, alive: bool) -> int:
        if alive:
            if 0 <= self.acc <= 16:
                return 0
            if 32 < self.acc <= 48:
                return 2
            else:
                return 1
        else:
            if 90 <= self.dead_counter <= 120:
                return 0
            if 60 <= self.dead_counter < 90:
                return 1
            if 30 <= self.dead_counter < 60:
                return 2
            if 0 < self.dead_counter < 30:
                return 3
        
    def draw_die_state(self, screen: Surface):
        path = "assets/images/pac-man"
        frames = ["1.png", "2.png", "3.png", "4.png"]
        current_frame = self._get_current_frame(False)
        screen.blit(pygame.image.load(f"{path}_dead/{frames[current_frame]}").convert_alpha(), (self.dead_position))

    def draw(self, screen: Surface) -> None:
        path = "assets/images/pac-man"
        if (self.dead_counter > 0):
            self.draw_die_state(screen)
            return
        
        frames = ["1.png", "2.png", "3.png"]
        x_px, y_px = self.position
        current_frame = self._get_current_frame(True)
        if self.current_direction == Direction.SOUTH:
            screen.blit(
                pygame.image.load(
                    f"{path}_down/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px),
            )
        elif self.current_direction == Direction.EAST:
            screen.blit(
                pygame.image.load(
                    f"{path}_right/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px),
            )
        elif self.current_direction == Direction.NORTH:
            screen.blit(
                pygame.image.load(
                    f"{path}_up/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px),
            )
        else:
            screen.blit(
                pygame.image.load(
                    f"{path}_left/{frames[current_frame]}"
                ).convert_alpha(),
                (x_px, y_px),
            )

    def update_position(self) -> bool:
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
                if (self.next_direction
                   and self._can_move(self.next_direction)):
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
            if 0 <= x + 1 <= self.maze.config.width - 1 and not self.maze.grid[y][x].east:
                return (y, x + 1)
            return None
        elif direction == Direction.WEST:
            if 0 <= x - 1 <= self.maze.config.width - 1 and not self.maze.grid[y][x].west:
                return (y, x - 1)
            return None

    def request_move(self, direction: Direction) -> None:
        if not self.target and self._can_move(direction):
            self.target = self._can_move(direction)
            self.current_direction = direction
        else:
            self.next_direction = direction

    def eat_current_cell(self) -> None | PacgumType:
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
        self.current_cell = self.start_cell
        self.position = self.respawn_position
        self.acc = 0
        self.target = None
        self.current_direction = None
        self.next_direction = None

    def lose_life(self) -> bool:
        self.lives -= 1
        return self.lives == 0

    def add_score(self, score: int) -> None:
        self.score += score
