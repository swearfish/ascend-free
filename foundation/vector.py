import math


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

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()
