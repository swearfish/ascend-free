import pygame.transform
from pygame.surface import Surface

from foundation.area import Area
from foundation.ascendancy_exception import AscendancyException
from foundation.vector import Vec2


class ShapeRenderer:
    def __init__(self, image, size=None):
        if isinstance(image, Surface):
            self._orig_img: Surface = image
        elif isinstance(image, ShapeRenderer):
            self._orig_img: Surface = image.surface
        else:
            raise AscendancyException('ShapeRenderer requires a shape or surface')
        self.surface = self._orig_img
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

    def draw(self, screen: Surface, pos: Vec2, area: Area = None):
        if area is not None:
            screen.blit(self.surface, pos.as_tuple(), area.as_tuple())
        else:
            screen.blit(self.surface, pos.as_tuple())


class Sprite:
    def __init__(self, image: ShapeRenderer | Surface, pos=Vec2(0, 0), center=Vec2(0, 0), size=None):
        if isinstance(image, ShapeRenderer):
            self.shape = image
        else:
            self.shape = ShapeRenderer(image)
        if size is not None:
            self.shape = ShapeRenderer(self.shape, size)
        self._pos = Vec2(0,0)
        self._center = center
        self.move(pos)

    @property
    def position(self) -> Vec2:
        return self._pos + self._center

    def move(self, pos: Vec2):
        self._pos = pos - self._center

    def move_by(self, delta: Vec2):
        self._pos += delta

    def draw(self, screen: Surface):
        self.shape.draw(screen, self._pos)
