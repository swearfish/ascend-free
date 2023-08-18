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

    @property
    def z(self):
        return self[2]


class Vec3D(Vector):
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        super().__init__(Vec3, value=[x, y, z, w])

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @property
    def w(self):
        return self[3]

    def as_vec3(self) -> Vec3:
        return Vec3(self[0], self[1], self[2])

    @staticmethod
    def from_vec3(orig: Vec3):
        return Vec3D(orig.x, orig.y, orig.z)