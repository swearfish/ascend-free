import math
import random

from engine import FileSystem
from foundation.gcom import component_resolve, Component
from foundation.vector_3d import Vec3


@component_resolve
class StarMap(Component):
    file_system: FileSystem

    def __init__(self):
        pass


class Star:
    def __init__(self, name: str, pos: Vec3, color: int):
        self._name = name
        self._pos = pos
        self._color = color


def generate_star_cluster(radius: int, num_stars: int):
    def is_in_sphere(x, y, z, radius):
        return x ** 2 + y ** 2 + z ** 2 <= radius ** 2

    def random_spherical_coordinates(radius):
        theta = random.uniform(0, 2 * math.pi)
        phi = math.acos(random.uniform(-1, 1))
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        return x, y, z

    stars = []
    for i in range(num_stars):
        # Generate a random point on the sphere
        x, y, z = random_spherical_coordinates(radius)
        while not is_in_sphere(x, y, z, radius):
            x, y, z = random_spherical_coordinates(radius)
        # Assign a random color
        stars.append(Vec3(x, y, z))

    return stars
