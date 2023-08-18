import pygame.draw
from pygame import Surface, Color

from engine.gui import Canvas
from foundation import Area, Vec2
from game.logic.star_map import StarMap


class StarMapRenderer(Canvas):
    def __init__(self, parent, area: Area, star_map: StarMap):
        super().__init__(parent, area)
        self.star_map = star_map

    def on_draw(self, screen: Surface, pos: Vec2):
        pygame.draw.rect(screen, [0xFF, 0x00, 0x00], pos.as_tuple(), self.area.size.as_tuple())
        pass