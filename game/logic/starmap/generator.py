from game.logic.starmap.point_generator import RandomSphericalPointGenerator
from game.logic.starmap.star import Star


def _generate_star_cluster(radius: int, num_stars: int, names: list[str],
                           stats: dict[str, tuple[float, float]]) -> list[Star]:
    stars: list[Star] = []
    type_limits = [int(num_stars * x[0] / 100) for x in stats.values()]
    type_limit = type_limits[0]
    star_type = 0
    # point_generator = BalancedSphericalPointGenerator(radius, num_stars)
    point_generator = RandomSphericalPointGenerator(radius)
    for i in range(num_stars):
        # Generate a random point on the sphere
        # Assign a random color
        pos = point_generator.next()
        name = names[i]
        if type_limit <= 0:
            star_type = (star_type + 1) % len(type_limits)
            type_limit = type_limits[star_type]
        else:
            type_limit -= 1
        stars.append(Star(name, pos, star_type))

    return stars
