class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __iter__(self):
        return iter((self.x, self.y, self.width, self.height))

    def collidepoint(self, position: tuple[int, int]):
        point_x, point_y = position

        in_x = self.x <= point_x < (self.x + self.width)
        in_y = self.y <= point_y < (self.y + self.height)

        return in_x and in_y

    @property
    def centerx(self):
        return self.x + (self.width // 2)

    @centerx.setter
    def centerx(self, value):
        self.x = value - (self.width // 2)

    @property
    def centery(self):
        return self.y + (self.height // 2)

    @centery.setter
    def centery(self, value):
        self.y = value - (self.height // 2)

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        self.y = value
