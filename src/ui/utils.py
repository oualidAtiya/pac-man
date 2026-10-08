from collections.abc import Iterator


class Rectangle:
    """A simple rectangle defined by its top-left corner and its size.

    It offers a small part of the pygame ``Rect`` interface: center and
    top properties, a point collision test, and iteration over its
    values so it can be turned into a tuple.

    Attributes:
        x: Horizontal position of the left side.
        y: Vertical position of the top side.
        width: Width of the rectangle.
        height: Height of the rectangle.
    """

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """Create a rectangle.

        Args:
            x: Horizontal position of the left side.
            y: Vertical position of the top side.
            width: Width of the rectangle.
            height: Height of the rectangle.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __iter__(self) -> Iterator:
        """Iterate over the rectangle values.

        Returns:
            An iterator over ``(x, y, width, height)``, so that
            ``tuple(rect)`` gives those four values.
        """
        return iter((self.x, self.y, self.width, self.height))

    def collidepoint(self, position: tuple[int, int]) -> bool:
        """Check whether a point is inside the rectangle.

        The left and top sides are included, the right and bottom
        sides are excluded.

        Args:
            position: The (x, y) position of the point to test.

        Returns:
            True if the point is inside the rectangle, False otherwise.
        """
        point_x, point_y = position

        in_x = self.x <= point_x < (self.x + self.width)
        in_y = self.y <= point_y < (self.y + self.height)

        return in_x and in_y

    @property
    def centerx(self) -> int:
        """Get the horizontal position of the rectangle center."""
        return self.x + (self.width // 2)

    @centerx.setter
    def centerx(self, value: int) -> None:
        """Move the rectangle so its horizontal center is ``value``."""
        self.x = value - (self.width // 2)

    @property
    def centery(self) -> int:
        """Get the vertical position of the rectangle center."""
        return self.y + (self.height // 2)

    @centery.setter
    def centery(self, value: int) -> None:
        """Move the rectangle so its vertical center is ``value``."""
        self.y = value - (self.height // 2)

    @property
    def top(self) -> int:
        """Get the vertical position of the top side."""
        return self.y

    @top.setter
    def top(self, value: int) -> None:
        """Move the rectangle so its top side is at ``value``."""
        self.y = value
