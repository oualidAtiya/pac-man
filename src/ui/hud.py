import pygame
from pygame import Surface

from src.game.state import GameState


class HUD:
    def __init__(self) -> None:
        self.digits = {
            str(i): pygame.image.load(
                f"./assets/images/digits/{i}.png"
            ).convert_alpha()
            for i in range(10)
        }
        self.level = pygame.image.load(
            "./assets/images/hud/level.png"
        ).convert_alpha()
        self.live = pygame.image.load(
            "./assets/images/hud/live.png"
        ).convert_alpha()
        self.score = pygame.image.load(
            "./assets/images/hud/score.png"
        ).convert_alpha()
        self.time = pygame.image.load(
            "./assets/images/hud/time.png"
        ).convert_alpha()
        self.super_gum_time = pygame.image.load(
            "./assets/images/hud/super_gum_time.png"
        ).convert_alpha()

    def _draw_score(
        self, screen: Surface, score: int, corr: tuple[int, int]
    ) -> None:
        x, y = corr
        screen.blit(self.score, (x, y))
        self._draw_number(screen, score, (x + 140, y))

    def _draw_number(
        self, screen: Surface, number: int, corr: tuple[int, int]
    ) -> None:
        x, y = corr
        number_str = str(number)
        for digit in number_str:
            screen.blit(self.digits[digit], (x, y))
            x += 28

    def _draw_remain_time(
        self, screen: Surface, time: int, corr: tuple[int, int]
    ) -> None:
        x, y = corr
        screen.blit(self.time, (x, y))
        self._draw_number(screen, time, (x + 120, y))

    def _draw_super_time(
        self, screen: Surface, time: int, corr: tuple[int, int]
    ) -> None:
        x, y = corr
        screen.blit(self.super_gum_time, (x, y))
        self._draw_number(screen, int(time), (x + 230, y))

    def _draw_remain_lives(
        self, screen: Surface, lives: int, corr: tuple[int, int]
    ) -> None:
        x, y = corr
        for _ in range(lives):
            screen.blit(self.live, (x, y))
            x += 40

    def draw(self, screen: Surface, state: GameState) -> None:
        player = state.player
        maze = state.maze
        height_px, width_px = maze.height_maze_px, maze.width_maze_px
        self._draw_score(
            screen, player.score, (maze.offest_x, maze.offest_y - 50)
        )
        self._draw_remain_lives(
            screen,
            player.lives,
            (maze.offest_x, maze.offest_y + height_px + 50),
        )
        self._draw_remain_time(
            screen,
            state.time_remaining,
            (maze.offest_x + width_px - 150, maze.offest_y + height_px + 50),
        )
        self._draw_current_level(
            screen,
            state.level,
            (
                (maze.offest_x - 70) + width_px // 2,
                maze.offest_y + height_px + 50,
            ),
        )
        if state.super_pacgum_timer > 0:
            self._draw_super_time(
                screen,
                int(state.super_pacgum_timer),
                (maze.offest_x + width_px - 250, maze.offest_y - 50),
            )

    def _draw_current_level(
        self, screen: Surface, level: int, corr: tuple[int, int]
    ) -> None:
        x, y = corr
        screen.blit(self.level, (x, y))
        self._draw_number(screen, level, (x + 140, y))
