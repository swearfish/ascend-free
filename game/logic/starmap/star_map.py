import random

from engine import FileSystem
from foundation.gcom import auto_wire
from game.game_const import COSMOS_RADIUS
from game.vis.language import Language

from .generator import _generate_star_cluster
from .star import Star, StarLane


@auto_wire
class StarMap:
    file_system: FileSystem
    language: Language

    def __init__(self, cluster_size):
        self.stat = {}
        self.star_names = self.file_system.read_lines('names.txt', skip_empty_lines=True)
        self.stars: list[Star] = []
        random.shuffle(self.star_names)
        # noinspection SpellCheckingInspection
        starstat_txt: list[str] = self.file_system.read_lines('starstat.txt', skip_empty_lines=True)
        self._fill_star_stat_from_txt(starstat_txt)
        self.generate_cluster(cluster_size)

    def generate_cluster(self, cluster_size):
        self.stars = _generate_star_cluster(COSMOS_RADIUS, cluster_size, self.star_names, self.stat)
        self._generate_star_lanes()

    def _generate_star_lanes(self):
        for star in self.stars:
            adjacent = self._get_adjacent_stars(star)
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

    def _fill_star_stat_from_txt(self, star_stat_txt):
        for line in star_stat_txt:
            parts = list(filter(lambda x: 0 < len(x), line.split(' ')))
            type_id = parts[0]
            percent = float(parts[1])
            lanes = float(parts[3])
            self.stat[type_id] = (percent, lanes)

    def _get_adjacent_stars(self, star):
        result = [(x, x.distance_to(star)) for x in self.stars]
        result = sorted(result, key=lambda x: x[1])
        result = [x[0] for x in result]
        return result

    @property
    def radius(self):
        return COSMOS_RADIUS

    @property
    def cluster_size(self):
        return len(self.stars)


def is_in_sphere(x, y, z, radius):
    return x ** 2 + y ** 2 + z ** 2 <= radius ** 2
