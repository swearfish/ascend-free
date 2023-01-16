import math
from typing import Optional


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert isinstance(other, (int, float))
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        assert isinstance(other, (int, float))
        return Vec2(self.x / other, self.y / other)

    def __len__(self):
        return math.sqrt(self.x*self.x + self.y * self.y)

    def to_tuple(self):
        return self.x, self.y


class Area:
    def __init__(self, top_left: Vec2, bottom_right: Optional[Vec2] = None, size: Optional[Vec2] = None):
        self.top_left = top_left
        if bottom_right is not None:
            assert size is None
            self.bottom_right = bottom_right
        elif size is not None:
            assert bottom_right is None
            self.bottom_right = self.top_left + size
        else:
            assert False, "either size or bottom_right is required"

    @property
    def left(self):
        return self.top_left.x

    @property
    def top(self):
        return self.top_left.y

    @property
    def right(self):
        return self.bottom_right.x

    @property
    def bottom(self):
        return self.bottom_right.y

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top
