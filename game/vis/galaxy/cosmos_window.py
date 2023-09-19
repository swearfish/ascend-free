import math
from typing import Optional

import pygame.draw
from pygame import Surface

from engine.gui import Control
from engine.resource_manager import ResourceManager
from foundation import Area, Vec2, Vec3
from foundation.gcom import auto_wire
from foundation.soft_3d import project_3d_to_2d, rotate_3d_around_y
from game.logic.starmap import Star
from game.logic.starmap.star_map import StarMap


@auto_wire
class CosmosWindow(Control):
    resource_manager: ResourceManager

    def __init__(self, parent, area: Area, star_map: StarMap = None):
        super().__init__(parent, area)
        self.star_map = star_map if star_map is not None else StarMap(50)
        self.stars = self.resource_manager.shape_from_file("data/cos_star.shp")
        self.rot_y = 0
        self.zoom = 1.0
        self.animate = False
        self.transparent = False
        self.star_2d_pos = []
        self.selected_star: Optional[Star] = None

    def on_draw(self, screen: Surface, pos: Vec2):
        if not self.transparent:
            pygame.draw.rect(screen, [0x00, 0x00, 0x00], self.area.new_origin(pos).as_tuple())
        if self.star_map is None:
            return
        center = Vec2(pos.x + self.area.width / 2, pos.y + self.area.height / 2)
        camera_focal_width = 15.0
        camera = Vec3(0, 0, self.star_map.radius * 2)
        self.star_2d_pos = []
        for star in self.star_map.stars:
            star_3d_pos = rotate_3d_around_y(star.pos, self.rot_y)
            star_3d_pos -= camera
            star_2d_pos = project_3d_to_2d(star_3d_pos, camera_focal_width, 1.0)
            dist = star_3d_pos.z / camera.z
            dist_index = 3-int(max(0, min(3, (dist + 0.25) * -3)))
            shape_index = star.type*4 + dist_index
            if star_2d_pos is not None:
                # self.stars.draw(screen, center + star_2d_pos * camera_focal_width, shape_index)
                star_2d_pos = center + star_2d_pos * self.zoom
                self.stars.draw(screen, star_2d_pos, shape_index)
                self.star_2d_pos.append((star_2d_pos, star))

    def on_update(self, total_time: float, frame_time: float):
        if self.animate:
            self.rot_y += math.pi / 180 * frame_time * 0.1
            if 2*math.pi < self.rot_y:
                self.rot_y -= 2*math.pi

    def on_mouse_move(self, mouse_pos: Vec2) -> bool:
        star_width = 6
        selected_star = None
        selected_star_dist = 1000
        for star_2d_pos, star in self.star_2d_pos:
            dist_vec: Vec2 = star_2d_pos - mouse_pos
            star_dist = abs(dist_vec.length)
            if star_dist < star_width and (selected_star is None or star_dist < selected_star_dist):
                selected_star = star
                selected_star_dist = star_dist
        self.selected_star = selected_star
        if selected_star:
            return True
        return False
