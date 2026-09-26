import pygame
from pygame import Surface

from src.config.models import GameConfig
from src.maze.adapter import MazeAdapter


class Maze:
    def __init__(self, config: GameConfig) -> None:
        self.grid = MazeAdapter(config).generate_maze()
        self.config = config
        self.width = config.width
        self.height = config.height

    def draw(self, screen: Surface) -> None:
        corners = {
            i: pygame.image.load(
                f"assets/images/corners/{i}x32.png"
            ).convert_alpha()
            for i in range(1, 17)
        }

        corner_rect = corners[1].get_rect()
        cell_width = corner_rect.width
        cell_heigh = corner_rect.height

        start_x = (screen.get_width() // 2) - (self.width * cell_width)
        start_y = (screen.get_height() // 2) - (self.height * cell_heigh)

        x_px = start_x
        y_px = start_y

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                west_cell = None
                north_cell = None
                east_cell = None
                south_cell = None
                if x > 0:
                    west_cell = self.grid[y][x - 1]
                if y > 0:
                    north_cell = self.grid[y - 1][x]
                if x < self.width - 1:
                    east_cell = self.grid[y][x + 1]
                if y < self.height - 1:
                    south_cell = self.grid[y + 1][x]

                screen.blit(
                    corners[cell.get_nw_corner(north_cell, west_cell)],
                    (x_px, y_px),
                )
                screen.blit(
                    corners[cell.get_ne_corner(north_cell, east_cell)],
                    (x_px + cell_width * 2, y_px),
                )
                screen.blit(
                    corners[cell.get_se_corner(east_cell, south_cell)],
                    (x_px + cell_width * 2, y_px + cell_width * 2),
                )
                screen.blit(
                    corners[cell.get_sw_corner(west_cell, south_cell)],
                    (x_px, y_px + cell_width * 2),
                )
                if cell.north:
                    screen.blit(corners[6], (x_px + cell_width, y_px))
                if cell.south:
                    screen.blit(
                        corners[6], (x_px + cell_width, y_px + cell_width * 2)
                    )
                if cell.east:
                    screen.blit(
                        corners[5], (x_px + cell_width * 2, y_px + cell_width)
                    )
                if cell.west:
                    screen.blit(corners[5], (x_px, y_px + cell_width))
                x_px += cell_width * 2
            y_px += cell_width * 2
            x_px = start_x
