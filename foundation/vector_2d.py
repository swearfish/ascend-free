from foundation.vector import Vector


class Vec2(Vector):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(Vec2, value=[x, y])

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def w(self):
        return self.x

    @property
    def h(self):
        return self.y
