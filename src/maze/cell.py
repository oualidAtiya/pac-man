class Cell:
    def __init__(self, cell_value: int) -> None:
        self.north = (cell_value & 1) != 0
        self.east = (cell_value & 2) != 0
        self.south = (cell_value & 4) != 0
        self.west = (cell_value & 8) != 0
        self.is_42 = cell_value == 15

    def __repr__(self):
        return f"(n={self.north}, e={self.east}, s={self.south}), w={self.west}"
