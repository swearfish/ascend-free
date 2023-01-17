from foundation.vector import Vec2


class Area:
    def __init__(self, top_left: Vec2, size: Vec2):
        self.top_left = top_left
        self.size = size

    @property
    def left(self):
        return self.top_left.x

    @property
    def top(self):
        return self.top_left.y

    @property
    def bottom_right(self) -> Vec2:
        return self.top_left + self.size

    @property
    def right(self):
        return self.bottom_right.x

    @property
    def bottom(self):
        return self.bottom_right.y

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    def to_tuple(self):
        return self.left, self.top, self.width, self.height

    def contains(self, v: Vec2) -> bool:
        return self.left <= v.x <= self.right and self.top <= v.y <= self.bottom

    def __str__(self):
        return f'({self.left}, {self.top}, {self.right}, {self.bottom}) x ({self.width}, {self.height})'

    def __repr__(self):
        return self.__str__()

def area_with_size_vec(top_left: Vec2, size: Vec2) -> Area:
    return Area(top_left, size)


def area_from_rect_vec(top_left: Vec2, bottom_right: Vec2) -> Area:
    size = bottom_right - top_left
    return area_with_size_vec(top_left, size)


def area_with_size(x, y, width, height) -> Area:
    return Area(Vec2(x, y), Vec2(width, height))


def area_from_rect(x1, y1, x2, y2) -> Area:
    width = x2 - x1 + 1
    height = y2 - y1 + 1
    return area_with_size(x1, y1, width, height)
