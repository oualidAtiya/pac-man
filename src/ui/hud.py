from pygame import Surface
import pygame
from src.game.state import GameState
from src.maze.maze import Maze


class HUD:
    def __init__(self) -> None:
        self.digits = {
            str(i): pygame.image.load(f"./assets/images/digits/{i}.png").convert_alpha() for i in range(10)
        }
        self.high_score = pygame.image.load("./assets/images/high_score.png").convert_alpha()
        self.level = pygame.image.load("./assets/images/level.png").convert_alpha()
        self.live = pygame.image.load("./assets/images/live.png").convert_alpha()
        self.score = pygame.image.load("./assets/images/score.png").convert_alpha()
        self.time = pygame.image.load("./assets/images/time.png").convert_alpha()
        self.super_gum_time = pygame.image.load("./assets/images/super_gum_time.png").convert_alpha()

    def _draw_score(self, screen: Surface, score: int, corr: tuple[int, int]) -> None:
        x, y = corr
        screen.blit(self.score, (x, y))
        self._draw_number(screen, score, (x+140, y))

    def _draw_number(self, screen: Surface, number: int, corr: tuple[int, int]) -> None:
        x, y = corr
        number = str(number)
        for digit in number:
            screen.blit(self.digits[digit], (x, y))
            x+=28

    def _draw_remain_time(self, screen: Surface, time: int, corr: tuple[int, int]) -> None:
        x, y = corr
        screen.blit(self.time, (x, y))
        self._draw_number(screen, time, (x+120, y))


    def _draw_super_time(self, screen: Surface, time: int, corr: tuple[int, int]) -> None:
        x, y = corr
        screen.blit(self.super_gum_time, (x, y))
        self._draw_number(screen, int(time), (x+230, y))

    def _draw_remain_lives(self, screen: Surface, lives: int, corr: tuple[int, int]) -> None:
        x, y = corr
        for _ in range(lives):
            screen.blit(self.live, (x, y))
            x+=40

    def draw(self, screen: Surface, state: GameState) -> None:
        self._draw_score(screen, state.player.score, (state.maze.offest_x, state.maze.offest_y-50))
        self._draw_remain_lives(screen, state.player.lives, (state.maze.offest_x, state.maze.offest_y+state.maze.height_maze_px+50))
        self._draw_remain_time(screen, state.time_remaining, (state.maze.offest_x+state.maze.width_maze_px-150, state.maze.offest_y+state.maze.height_maze_px+50))
        self._draw_current_level(screen, state.level, ((state.maze.offest_x-70)+state.maze.width_maze_px//2, state.maze.offest_y+state.maze.height_maze_px+50))
        if (state.super_pacgum_timer > 0):
            self._draw_super_time(screen, state.super_pacgum_timer, (state.maze.offest_x+state.maze.width_maze_px-250, state.maze.offest_y-50))

    def _draw_current_level(self, screen: Surface, level: int, corr: tuple[int, int]) -> None:
        x, y = corr
        screen.blit(self.level, (x, y))
        self._draw_number(screen, level, (x+140, y))