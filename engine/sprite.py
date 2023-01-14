import pygame.transform
from pygame.surface import Surface

from engine.game_engine import the_engine


class Sprite:
    def __init__(self, image, pos = (0, 0), center = (0, 0), size = None, opacity = 255):
        self._orig_img: Surface = image
        self._pos = (0, 0)
        self._center = center
        self._img = self._orig_img
        self.move(pos)
        if size is not None:
            self.scale(size)

    @property
    def position(self):
        return self._pos[0] + self._center[0], self._pos[1] + self._center[1]

    def move(self, pos):
        self._pos = (pos[0] - self._center[0], pos[1] - self._center[1])

    def move_by(self, delta):
        self._pos[0] += delta[0]
        self._pos[1] += delta[1]

    def scale(self, size):
        if size is not None:
            self._img = pygame.transform.scale(self._orig_img, size)

    def set_opacity(self, opacity: int = 255):
        assert 0 <= opacity < 256
        self._img.set_alpha(opacity)

    def draw(self, screen: Surface):
        screen.blit(self._img, self._pos)