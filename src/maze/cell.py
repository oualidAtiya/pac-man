class Cell:
    def __init__(self, cell_value: int) -> None:
        self.north = (cell_value & 1) != 0
        self.east = (cell_value & 2) != 0
        self.south = (cell_value & 4) != 0
        self.west = (cell_value & 8) != 0
        self.is_42 = cell_value == 15

    def __repr__(self):
        return f"(n={self.north}, e={self.east}, s={self.south}, w={self.west})"

    @staticmethod
    def get_corner(up: bool, right: bool, bottom: bool, left: bool) -> int:
        if up and right and bottom and left:
            return 11
        if up and right and bottom and not left:
            return 8
        if up and not right and bottom and  left:
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
        if not up and not right and  not bottom and left:
            return 9
        if not up and  right and  not bottom and not left:
            return 14
        if not up and right and not bottom and left:
            return 6
        return 10

    def get_nw_corner(self, north_cell: any, west_cell: any) -> int:
        up = north_cell.west if north_cell else False
        bottom = self.west
        left = west_cell.north if west_cell else False
        right = self.north
        return Cell.get_corner(up, right, bottom, left)

    def get_ne_corner(self, north_cell: any, east_cell: any) -> int:
        up = north_cell.east if north_cell else False
        bottom = self.east
        left = self.north
        right = east_cell.north if east_cell else False
        return Cell.get_corner(up, right, bottom, left)

    def get_se_corner(self, east_cell: any, south_cell: any) -> int:
        up = self.east
        bottom = south_cell.east if south_cell else False
        left = self.south
        right = east_cell.south if east_cell else False
        return Cell.get_corner(up, right, bottom, left)

    def get_sw_corner(self, west_cell: any, south_cell: any) -> int:
        up = self.west
        bottom = south_cell.west if south_cell else False
        left = west_cell.south if west_cell else False
        right = self.south
        return Cell.get_corner(up, right, bottom, left)
