from collections import deque

import pygame
from pygame import Surface

from src.config.models import GameConfig
from src.game.direction import Direction
from src.maze.adapter import MazeAdapter


class Maze:
    def __init__(self, config: GameConfig) -> None:
        self.grid = MazeAdapter(config).generate_maze()
        self.config = config
        self.default = config.height, config.width
        self.width_maze_px = None
        self.height_maze_px = None
        self.offest_x = None
        self.offest_y = None
        self.set_height_width_px()
        self.set_offests()
        self.set_cells_positions()


    def set_height_width_px(self) -> None:
        self.width_maze_px = (32 * self.config.width + 1) + (32 * self.config.width)
        self.height_maze_px = (32 * self.config.height + 1) + (32 * self.config.height)

    def set_offests(self) -> None:
        self.offest_x = (2000 // 2) - (self.config.width * 32)
        self.offest_y = (1500 // 2) - (self.config.height * 32)

    def can_move(self, col: int, row: int, direction: Direction) -> bool:
        if direction == Direction.NORTH:
            return row - 1 >= 0 and not self.grid[row][col].north

        if direction == Direction.SOUTH:
            return row + 1 < self.config.height and not self.grid[row][col].south

        if direction == Direction.WEST:
            return col - 1 >= 0 and not self.grid[row][col].west

        if direction == Direction.EAST:
            return col + 1 < self.config.width and not self.grid[row][col].east

    def distance(
        self,
        first_position: tuple[int, int],
        second_position: tuple[int, int],
    ) -> int | None:
        queue = deque([(first_position, 0)])
        visited = {first_position}

        while queue:
            (col, row), curr_distance = queue.popleft()

            if (col, row) == second_position:
                return curr_distance

            for direction in Direction:
                if not self.can_move(col, row, direction):
                    continue

                if direction == Direction.NORTH:
                    next_position = col, row - 1
                elif direction == Direction.SOUTH:
                    next_position = col, row + 1
                elif direction == Direction.WEST:
                    next_position = col - 1, row
                elif direction == direction.EAST:
                    next_position = col + 1, row

                if next_position in visited:
                    continue

                next_distance = curr_distance + 1

                visited.add(next_position)
                queue.append((next_position, next_distance))

        return None

    def regenerate_maze(self, next_level: bool) -> None:
        if next_level:
            self.config.width += 1
            self.config.height += 1
        else:
            self.config.height = self.default[0]
            self.config.width = self.default[1]
        self.grid = MazeAdapter(self.config).generate_maze()
        self.set_height_width_px()
        self.set_offests()
        self.set_cells_positions()

    def set_cells_positions(self) -> None:
        x_px = self.offest_x
        y_px = self.offest_y
        for y in range(self.config.height):
            for x in range(self.config.width):
                cell = self.grid[y][x]
                cell.content_position_px = (x_px + 32, y_px + 32)
                x_px += 32 * 2
            y_px += 32 * 2
            x_px = self.offest_x

    def draw(self, screen: Surface) -> None:
        corners = {
            i: pygame.image.load(
                f"assets/images/corners/{i}x32.png"
            ).convert_alpha()
            for i in range(1, 17)
        }
        cell_width = 32

        x_px = self.offest_x
        y_px = self.offest_y

        for y in range(self.config.height):
            for x in range(self.config.width):
                cell = self.grid[y][x]
                west_cell = None
                north_cell = None
                east_cell = None
                south_cell = None
                if x > 0:
                    west_cell = self.grid[y][x - 1]
                if y > 0:
                    north_cell = self.grid[y - 1][x]
                if x < self.config.width - 1:
                    east_cell = self.grid[y][x + 1]
                if y < self.config.height - 1:
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
