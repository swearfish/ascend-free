import pygame.transform
from pygame.surface import Surface

from foundation.area import Area
from foundation.ascendancy_exception import AscendancyException
from foundation.vector_2d import Vec2


class SurfaceRenderer:
    def __init__(self, image, size=None, center: Vec2 = None):
        if isinstance(image, Surface):
            self._orig_img: Surface = image
        elif isinstance(image, SurfaceRenderer):
            self._orig_img: Surface = image.surface
        else:
            raise AscendancyException('SurfaceRenderer requires another renderer or surface')
        self.surface = self._orig_img
        self.center = Vec2(0, 0) if center is None else center
        if size is not None:
            self.scale(size)

    @property
    def width(self) -> int:
        return self.surface.get_width()

    @property
    def height(self) -> int:
        return self.surface.get_height()

    @property
    def size(self) -> Vec2:
        return Vec2(self.width, self.height)

    def scale(self, size):
        if size is not None:
            self.surface = pygame.transform.scale(self._orig_img, size)

    def set_opacity(self, opacity: int = 255):
        assert 0 <= opacity < 256
        self.surface.set_alpha(opacity)

    def set_color_key(self, color=None):
        if color is None:
            color = self.surface.get_at((0, 0))
        self.surface.set_colorkey(color)

    def draw(self, screen: Surface, pos: Vec2, area: Area = None, center=False):
        if center:
            draw_pos = pos - self.center
        else:
            draw_pos = pos
        if area is not None:
            screen.blit(self.surface, draw_pos.as_tuple(), area.as_tuple())
        else:
            screen.blit(self.surface, draw_pos.as_tuple())
