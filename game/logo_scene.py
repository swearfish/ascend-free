import pygame as pg
from pygame.surface import SurfaceType, Surface

from engine.resource_manager import ResourceManager
from engine.scene import Scene


class LogoScene(Scene):
    def __init__(self):
        self.blending = None
        self.logo: Surface | None = None
        self.alpha = 0

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
        if total_time < 1000:
            self.alpha = total_time // 4
        elif total_time < 2000:
            self.alpha = 255
        elif total_time < 3000:
            self.alpha = (3000-total_time) // 4
        else:
            self.alpha = 0

    def draw(self, screen: Surface | SurfaceType):
        screen.fill((0,0,0))
        if 0 <= self.alpha < 256:
            self.logo.set_alpha(self.alpha)
            screen.blit(self.logo, (0,0))
