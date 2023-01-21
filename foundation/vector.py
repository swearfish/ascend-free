import math
from copy import copy


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self.x

    @property
    def h(self):
        return self.y

    def dup(self):
        return copy(self)

    def __eq__(self, other):
        if not isinstance(other, Vec2):
            return False
        return self._x == other._x and self._y == other._y

    def __add__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self._x - other._x, self._y - other._y)

    def __mul__(self, other):
        assert isinstance(other, (int, float))
        return Vec2(self._x * other, self._y * other)

    def __truediv__(self, other):
        assert isinstance(other, (int, float))
        return Vec2(self._x / other, self._y / other)

    def __len__(self):
        return math.sqrt(self._x * self._x + self._y * self._y)

    def as_tuple(self):
        return self._x, self._y

    def __str__(self):
        return f'({self._x}, {self._y})'

    def __repr__(self):
        return self.__str__()
