from typing import Any


class Cell:
    """A single maze cell, with its walls and its content.

    The walls are decoded from the integer given by the maze generator.
    A wall attribute is True when that wall is closed.

    Attributes:
        CELL_SIZE: Size of a cell in pixels.
        north: True if the north wall is closed.
        east: True if the east wall is closed.
        south: True if the south wall is closed.
        west: True if the west wall is closed.
        is_42: True if the cell belongs to the "42" pattern (all four
            walls closed).
        content_position_px: The (x, y) pixel position where the
            content of the cell (gums) is drawn.
        has_pacgum: True if the cell holds a normal pacgum.
        has_super_pacgum: True if the cell holds a super-pacgum.
    """

    CELL_SIZE = 32

    def __init__(self, cell_value: int) -> None:
        """Create a cell from the integer given by the generator.

        Bit 0 is the north wall, bit 1 the east wall, bit 2 the south
        wall and bit 3 the west wall. A value of 15 means the cell is
        part of the "42" pattern.

        Args:
            cell_value: The integer describing the closed walls.
        """
        self.north = (cell_value & 1) != 0
        self.east = (cell_value & 2) != 0
        self.south = (cell_value & 4) != 0
        self.west = (cell_value & 8) != 0
        self.is_42 = cell_value == 15
        self.content_position_px = (0, 0)
        self.has_pacgum = False
        self.has_super_pacgum = False

    @staticmethod
    def get_corner(up: bool, right: bool, bottom: bool, left: bool) -> int:
        """Get the corner type for the wall segments meeting at a point.

        Each argument tells if a wall segment leaves the corner point
        in that direction. The 16 possible combinations map to a
        number that identifies which corner image to draw.

        Args:
            up: True if a wall segment goes up from the point.
            right: True if a wall segment goes right from the point.
            bottom: True if a wall segment goes down from the point.
            left: True if a wall segment goes left from the point.

        Returns:
            The corner number, from 1 to 16. The value 10 is returned
            when no wall segment touches the point.
        """
        if up and right and bottom and left:
            return 11
        if up and right and bottom and not left:
            return 8
        if up and not right and bottom and left:
            return 13
        if not up and right and bottom and left:
            return 12
        if up and right and not bottom and left:
            return 7
        if not up and right and bottom and not left:
            return 2
        if up and not right and not bottom and left:
            return 4
        if up and right and not bottom and not left:
            return 1
        if not up and not right and bottom and left:
            return 3
        if up and not right and bottom and not left:
            return 5
        if not up and not right and bottom and not left:
            return 15
        if up and not right and not bottom and not left:
            return 16
        if not up and not right and not bottom and left:
            return 9
        if not up and right and not bottom and not left:
            return 14
        if not up and right and not bottom and left:
            return 6
        return 10

    def get_nw_corner(self, north_cell: Any, west_cell: Any) -> int:
        """Get the corner type of the top-left corner of this cell.

        Combines the walls of this cell with the matching walls of the
        northern and western neighbors.

        Args:
            north_cell: The cell above this one, or None if there is
                none.
            west_cell: The cell to the left of this one, or None if
                there is none.

        Returns:
            The corner number, as given by ``get_corner``.
        """
        up = north_cell.west if north_cell else False
        bottom = self.west
        left = west_cell.north if west_cell else False
        right = self.north
        return Cell.get_corner(up, right, bottom, left)

    def get_ne_corner(self, north_cell: Any, east_cell: Any) -> int:
        """Get the corner type of the top-right corner of this cell.

        Combines the walls of this cell with the matching walls of the
        northern and eastern neighbors.

        Args:
            north_cell: The cell above this one, or None if there is
                none.
            east_cell: The cell to the right of this one, or None if
                there is none.

        Returns:
            The corner number, as given by ``get_corner``.
        """
        up = north_cell.east if north_cell else False
        bottom = self.east
        left = self.north
        right = east_cell.north if east_cell else False
        return Cell.get_corner(up, right, bottom, left)

    def get_se_corner(self, east_cell: Any, south_cell: Any) -> int:
        """Get the corner type of the bottom-right corner of this cell.

        Combines the walls of this cell with the matching walls of the
        eastern and southern neighbors.

        Args:
            east_cell: The cell to the right of this one, or None if
                there is none.
            south_cell: The cell below this one, or None if there is
                none.

        Returns:
            The corner number, as given by ``get_corner``.
        """
        up = self.east
        bottom = south_cell.east if south_cell else False
        left = self.south
        right = east_cell.south if east_cell else False
        return Cell.get_corner(up, right, bottom, left)

    def get_sw_corner(self, west_cell: Any, south_cell: Any) -> int:
        """Get the corner type of the bottom-left corner of this cell.

        Combines the walls of this cell with the matching walls of the
        western and southern neighbors.

        Args:
            west_cell: The cell to the left of this one, or None if
                there is none.
            south_cell: The cell below this one, or None if there is
                none.

        Returns:
            The corner number, as given by ``get_corner``.
        """
        up = self.west
        bottom = south_cell.west if south_cell else False
        left = west_cell.south if west_cell else False
        right = self.south
        return Cell.get_corner(up, right, bottom, left)
