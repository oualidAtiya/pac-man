from src.config.models import GameConfig
from src.maze.adapter import MazeAdapter
import pygame


class Maze:
    def __init__(self, config: GameConfig) -> None:
        self.grid = MazeAdapter(config).generate_maze()
        self.config = config


    def draw(self, screen, start_x: int, start_y: int) -> None:
        corners = {
            i: pygame.image.load(f"images/corners/{i}x32.png").convert_alpha() for i in range(1, 17)
        }
        width = self.config.width
        height = self.config.height
        x_px = start_x
        y_px = start_y
        cell_size = 32
        for y in range(height):
            for x in range(width):
                cell = self.grid[y][x]
                west_cell = None
                north_cell = None
                east_cell = None
                south_cell = None
                if x > 0:
                    west_cell = self.grid[y][x - 1]
                if y > 0:
                    north_cell = self.grid[y - 1][x]
                if x < width - 1:
                    east_cell = self.grid[y][x + 1]
                if y < height - 1:
                    south_cell = self.grid[y + 1][x]

                screen.blit(corners[cell.get_nw_corner(north_cell, west_cell)], (x_px, y_px))
                screen.blit(corners[cell.get_ne_corner(north_cell, east_cell)], (x_px+cell_size*2, y_px))
                screen.blit(corners[cell.get_se_corner(east_cell, south_cell)], (x_px+cell_size*2, y_px+cell_size*2))
                screen.blit(corners[cell.get_sw_corner(west_cell, south_cell)], (x_px, y_px+cell_size*2))
                if cell.north:
                    screen.blit(corners[6], (x_px+cell_size, y_px))
                if cell.south:
                    screen.blit(corners[6], (x_px+cell_size, y_px+cell_size*2))
                if cell.east:
                    screen.blit(corners[5], (x_px+cell_size*2, y_px+cell_size))
                if cell.west:
                    screen.blit(corners[5], (x_px, y_px+cell_size))
                x_px += cell_size*2
            y_px += cell_size*2
            x_px = start_x
