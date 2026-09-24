class Cell:
    def __init__(self, north: bool, east: bool, west: bool, south: bool) -> None:
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.is_42 = False

    def __repr__(self):
        return f"(n={self.north}, e={self.east}, s={self.south}), w={self.west}"
