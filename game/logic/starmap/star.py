from foundation import Vec3

class Star:
    def __init__(self, name: str, pos: Vec3, star_type: int):
        self.name = name
        self.pos = pos
        self.type = star_type
        self.star_lanes: list[StarLane] = []

    def distance_to(self, other) -> float:
        return (self.pos - other.pos).length

class StarLane:
    def __init__(self, star1: Star, star2: Star, is_red_link: bool):
        self.star_1 = star1
        self.star_2 = star2
        self.is_red_link = is_red_link
        self.distance = self.star_1.distance_to(self.star_2)
