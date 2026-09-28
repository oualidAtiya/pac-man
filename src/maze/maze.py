import pygame
from pygame import Surface

from src.config.models import GameConfig
from src.game.direction import Direction
from src.maze.adapter import MazeAdapter


class Maze:
    def __init__(self, config: GameConfig) -> None:
        self.grid = MazeAdapter(config).generate_maze()
        self.config = config
        self.width = config.width
        self.height = config.height
        self.width_maze_px = (32 * config.width + 1) + (32 * config.width)
        self.height_maze_px = (32 * config.height + 1) + (32 * config.height)
        self.offest_x = (2000 // 2) - (self.width * 32)
        self.offest_y = (1500 // 2) - (self.height * 32)

    def can_move(self, col: int, row: int, direction: Direction) -> bool:
        if direction == Direction.NORTH:
            return row - 1 >= 0 and not self.grid[row][col].north

        if direction == Direction.SOUTH:
            return row + 1 < self.height and not self.grid[row][col].south

        if direction == Direction.WEST:
            return col - 1 >= 0 and not self.grid[row][col].west

        if direction == Direction.EAST:
            return col + 1 < self.width and not self.grid[row][col].east

    def draw(self, screen: Surface) -> None:
        corners = {
            i: pygame.image.load(
                f"assets/images/corners/{i}x32.png"
            ).convert_alpha()
            for i in range(1, 17)
        }

        corner_rect = corners[1].get_rect()
        cell_width = corner_rect.width

        x_px = self.offest_x
        y_px = self.offest_y

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                cell.gum_position = (x_px + 32, y_px + 32)
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
            x_px = self.offest_x
