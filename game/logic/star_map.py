import math
import random
from copy import copy

from engine import FileSystem
from foundation.gcom import auto_wire
from foundation.vector_3d import Vec3
from game.vis.language import Language


@auto_wire
class StarMap:
    file_system: FileSystem
    language: Language
    COSMOS_RADIUS = 500

    def __init__(self):
        self.star_names = self.file_system.read_lines('names.txt', skip_empty_lines=True)
        random.shuffle(self.star_names)
        starstat_txt = self.file_system.read_lines('starstat.txt', skip_empty_lines=True)
        self.stat = {}
        for line in starstat_txt:
            parts = list(filter(lambda x: 0 < len(x), line.split(' ')))
            type_id = parts[0]
            percent = float(parts[1])
            lanes = float(parts[3])
            self.stat[type_id] = (percent, lanes)
        self.stars = generate_star_cluster(StarMap.COSMOS_RADIUS, 50, self.star_names, self.stat)
        for star in self.stars:
            adjacent = self.get_adjacent_stars(star)
            adjacent = list(filter(lambda x: x != star, adjacent))
            no_lane = list(filter(lambda x: len(x.star_lanes) == 0, adjacent))
            if 0 == len(no_lane):
                continue
            lane0 = StarLane(star, no_lane[0], False)
            star.star_lanes.append(lane0)
            num_lanes = random.randint(1, 4) - len(star.star_lanes)
            prev = 0
            for i in range(0, num_lanes):
                is_red_link = random.randint(0, 3) == 0
                end_id = prev + random.randint(0, 3)
                if end_id >= len(no_lane):
                    break
                lane = StarLane(star, no_lane[end_id], is_red_link)
                prev = end_id
                star.star_lanes.append(lane)
        pass

    def get_adjacent_stars(self, star):
        result = [(x, x.distance_to(star)) for x in self.stars]
        result = sorted(result, key = lambda x: x[1])
        result = [x[0] for x in result]
        return result


class Star:
    def __init__(self, name: str, pos: Vec3, type: int):
        self.name = name
        self.pos = pos
        self.type = type
        self.star_lanes: list[StarLane] = []

    def distance_to(self, other) -> float:
        return (self.pos - other.pos).length


class StarLane:
    def __init__(self, star1: Star, star2: Star, is_red_link: bool):
        self.star_1 = star1
        self.star_2 = star2
        self.is_red_link = is_red_link
        self.distance = self.star_1.distance_to(self.star_2)


def generate_star_cluster(radius: int, num_stars: int, names: list[str],
                          stats: dict[str, tuple[float, float]]) -> list[Star]:
    def is_in_sphere(x, y, z, radius):
        return x ** 2 + y ** 2 + z ** 2 <= radius ** 2

    def random_spherical_coordinates(radius):
        theta = random.uniform(0, 2 * math.pi)
        phi = math.acos(random.uniform(-1, 1))
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        return x, y, z

    stars: list[Star] = []
    type_limits = [int(num_stars * x[0] / 100) for x in stats.values()]
    type_limit = type_limits[0]
    type = 0
    for i in range(num_stars):
        # Generate a random point on the sphere
        x, y, z = random_spherical_coordinates(radius)
        while not is_in_sphere(x, y, z, radius):
            x, y, z = random_spherical_coordinates(radius)
        # Assign a random color
        pos = Vec3(x, y, z)
        name = names[i]
        if type_limit <= 0:
            type = (type + 1) % len(type_limits)
            type_limit = type_limits[type]
        else:
            type_limit -= 1
        stars.append(Star(name, pos, type))

    return stars
