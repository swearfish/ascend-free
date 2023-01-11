import pygame as pg
from pygame.surface import SurfaceType, Surface

from engine.resource_manager import ResourceManager
from engine.scene import Scene


class LogoScene(Scene):
    def __init__(self):
        self.blending = None
        self.logo: Surface | None = None

    def enter(self):
        pass

    def exit(self):
        pass

    def load(self, res: ResourceManager):
        self.logo = res.read_gif('data/logo.gif')
        pass

    def unload(self):
        self.logo = None
        pass

    def update(self, total_time: float, frame_time: float):
        alpha = None
        if total_time < 1000:
            alpha = total_time // 4
        elif total_time < 2000:
            alpha = 255
        elif total_time < 3000:
            alpha = (3000-total_time) // 4
        else:
            alpha = 0
        if alpha is not None and 0 <= alpha < 256:
            self.logo.set_alpha(alpha)

    def draw(self, screen: Surface | SurfaceType):
        screen.fill((0,0,0))
        screen.blit(self.logo, (0,0))
