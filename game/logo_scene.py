from pygame.surface import SurfaceType, Surface

from engine.resource_manager import ResourceManager
from engine.scene import Scene

class LogoScene(Scene):
    def __init__(self):
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
        pass

    def draw(self, screen: Surface | SurfaceType):
        screen.fill((0,0,0))
        screen.blit(self.logo, (0, 0))
