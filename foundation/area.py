import copy

from foundation.vector_2d import Vec2


class Area:
    def __init__(self, top_left: Vec2, size: Vec2):
        self._top_left = top_left
        self._size = size

    @property
    def top_left(self):
        return self._top_left

    @property
    def size(self):
        return self._size

    @property
    def left(self):
        return self._top_left.x

    @property
    def top(self):
        return self._top_left.y

    @property
    def bottom_right(self) -> Vec2:
        return self._top_left + self._size

    @property
    def right(self):
        return self.bottom_right.x

    @property
    def bottom(self):
        return self.bottom_right.y

    @property
    def width(self):
        return self._size.x

    @property
    def height(self):
        return self._size.y

    @property
    def center(self) -> Vec2:
        return self.top_left + self.size / 2

    def new_origin(self, origin=Vec2(0, 0)):
        return Area(origin, self._size)

    def move_by(self, delta: Vec2):
        return self.new_origin(self.top_left + delta)

    def as_tuple(self):
        return self.left, self.top, self.width, self.height

    def dup(self):
        return copy.deepcopy(self)

    def contains(self, v: Vec2) -> bool:
        return self.left <= v.x <= self.right and self.top <= v.y <= self.bottom

    def __str__(self):
        return f'({self.left}, {self.top}, {self.right}, {self.bottom}) x ({self.width}, {self.height})'

    def __repr__(self):
        return self.__str__()


def area_with_size_vec(top_left: Vec2, size: Vec2) -> Area:
    return Area(copy.copy(top_left), copy.copy(size))


def area_from_rect_vec(top_left: Vec2, bottom_right: Vec2) -> Area:
    size = bottom_right - top_left
    return area_with_size_vec(top_left, size)


def area_with_size(x, y, width, height) -> Area:
    return Area(Vec2(x, y), Vec2(width, height))


def area_from_rect(x1, y1, x2, y2) -> Area:
    width = x2 - x1 + 1
    height = y2 - y1 + 1
    return area_with_size(x1, y1, width, height)
