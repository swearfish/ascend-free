import math
import random

from foundation import Vec3


class AbstractPointGenerator:

    def next(self) -> Vec3:
        return Vec3(0, 0, 0)


class RandomSphericalPointGenerator(AbstractPointGenerator):

    def __init__(self, radius: float):
        self.radius = radius

    def next(self) -> Vec3:
        theta = random.uniform(0, 2 * math.pi)
        phi = math.acos(random.uniform(-1, 1))
        distance = random.uniform(0, self.radius)
        x = distance * math.sin(phi) * math.cos(theta)
        y = distance * math.sin(phi) * math.sin(theta)
        z = distance * math.cos(phi)
        return Vec3(x, y, z)


class BalancedSphericalPointGenerator(AbstractPointGenerator):

    def __init__(self, radius: float, num_points: int):
        self.radius = radius
        self.increment = math.pi * (3 - math.sqrt(5))
        self.offset = 2 / num_points
        self.index = 0

    def next(self) -> Vec3:
        y = self.index * self.offset - 1 + (self.offset / 2)
        radius_xy = math.sqrt(1 - y * y)
        theta = self.index * self.increment

        x = math.cos(theta) * radius_xy
        z = math.sin(theta) * radius_xy

        # Scale the coordinates by the desired radius
        return Vec3(x, y, z) * self.radius
