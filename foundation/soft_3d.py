import math

from foundation import Vec3, Vec2


def project_3d_to_2d(pos: Vec3, focal_width: float, p: float) -> Vec2 | None:
    # Perform perspective projection
    p_corr = p + pos.z
    if p_corr == 0:
        return None
    return Vec2(
        pos.x * focal_width / p_corr,
        pos.y * focal_width / p_corr
    )


def rotate_3d_around_y(pos_3d: Vec3, angle: float) -> Vec3:
    x = pos_3d.x * math.cos(angle) + pos_3d.z * math.sin(angle)
    y = pos_3d.y
    z = -pos_3d.x * math.sin(angle) + pos_3d.z * math.cos(angle)
    return Vec3(x, y, z)


def project_logarithmically(value: float, max_value: float) -> float:
    # Perform logarithmic projection
    return (math.log(value + 1) / math.log(max_value + 1)) * 3
