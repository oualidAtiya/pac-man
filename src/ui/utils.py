from collections.abc import Iterator


class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __iter__(self) -> Iterator:
        return iter((self.x, self.y, self.width, self.height))

    def collidepoint(self, position: tuple[int, int]) -> bool:
        point_x, point_y = position

        in_x = self.x <= point_x < (self.x + self.width)
        in_y = self.y <= point_y < (self.y + self.height)

        return in_x and in_y

    @property
    def centerx(self) -> int:
        return self.x + (self.width // 2)

    @centerx.setter
    def centerx(self, value: int) -> None:
        self.x = value - (self.width // 2)

    @property
    def centery(self) -> int:
        return self.y + (self.height // 2)

    @centery.setter
    def centery(self, value: int) -> None:
        self.y = value - (self.height // 2)

    @property
    def top(self) -> int:
        return self.y

    @top.setter
    def top(self, value: int) -> None:
        self.y = value
