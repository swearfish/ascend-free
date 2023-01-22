from foundation.vector import Vector


class Vec3(Vector):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(Vec3, value=[x, y, z])

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def z(self):
        return self[2]
