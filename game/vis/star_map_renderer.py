import math

import pygame.draw
from pygame import Surface

from engine.gui import Canvas
from engine.resource_manager import ResourceManager
from foundation import Area, Vec2, Vec3
from foundation.gcom import auto_wire
from game.logic.star_map import StarMap


def project_3d_to_2d(pos: Vec3, scale: float, p: float) -> Vec2 | None:
    # Perform perspective projection
    p_corr = p + pos.z
    if p_corr == 0:
        return None
    return Vec2(
        pos.x * scale / p_corr,
        pos.y * scale / p_corr
    )


def rotate_3d_around_y(pos_3d: Vec3, angle: float) -> Vec3:
        x = pos_3d.x * math.cos(angle) + pos_3d.z * math.sin(angle)
        y = pos_3d.y
        z = -pos_3d.x * math.sin(angle) + pos_3d.z * math.cos(angle)
        return Vec3(x, y, z)


def project_logarithmically(value: float, max_value: float) -> float:
    # Perform logarithmic projection
    return (math.log(value + 1) / math.log(max_value + 1)) * 3


@auto_wire
class StarMapRenderer(Canvas):
    resource_manager: ResourceManager

    def __init__(self, parent, area: Area, star_map: StarMap):
        super().__init__(parent, area)
        self.star_map = star_map
        self.stars = self.resource_manager.shape_from_file("data/cos_star.shp")
        self.rot_y = 0

    def on_draw(self, screen: Surface, pos: Vec2):
        pygame.draw.rect(screen, [0x00, 0x00, 0x00], self.area.new_origin(pos).as_tuple())
        center = Vec2(pos.x + screen.get_width() / 2, pos.y + screen.get_height() / 2)
        scale = 15.0
        self.rot_y += math.pi / 360
        camera = Vec3(0, 0, StarMap.COSMOS_RADIUS * 2)
        for star in self.star_map.stars:
            star_3d_pos = rotate_3d_around_y(star.pos, self.rot_y)
            star_3d_pos -= camera
            star_2d_pos = project_3d_to_2d(star_3d_pos, scale, 1.0)
            dist = star_3d_pos.z / camera.z
            dist_index = 3-int(max(0, min(3, (dist + 0.25) * -3)))
            shape_index = star.type*4 + dist_index
            if star_2d_pos is not None:
                self.stars.draw(screen, center + star_2d_pos * scale, shape_index)

