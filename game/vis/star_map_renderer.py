import pygame.draw
from pygame import Surface

from engine.gui import Canvas
from engine.resource_manager import ResourceManager
from foundation import Area, Vec2
from foundation.gcom import auto_wire
from game.logic.star_map import StarMap


@auto_wire
class StarMapRenderer(Canvas):
    resource_manager: ResourceManager

    def __init__(self, parent, area: Area, star_map: StarMap):
        super().__init__(parent, area)
        self.star_map = star_map
        self.stars = self.resource_manager.shape_from_file("data/cos_star.shp")

    def on_draw(self, screen: Surface, pos: Vec2):
        pygame.draw.rect(screen, [0x22, 0x22, 0x22], self.area.new_origin(pos).as_tuple())
        center = Vec2(pos.x + screen.get_width() / 2, pos.y + screen.get_height() / 2)
        scale = 1.0
        for star in self.star_map.stars:
            star_2d_pos = Vec2(star.pos.x, star.pos.y)
            self.stars.draw(screen, center + star_2d_pos * scale, 3)
            pass
