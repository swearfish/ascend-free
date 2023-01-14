from engine.resource_manager import ResourceManager
from engine.scene import Scene
from engine.sprite import Sprite
from settings import SCREEN_SIZE


class LogoScene(Scene):
    def __init__(self):
        self.logo: Sprite | None = None

    def enter(self):
        pass

    def exit(self):
        pass

    def load(self, res: ResourceManager):
        logo_img = res.read_gif('data/logo.gif')
        self.logo = Sprite(logo_img, size=SCREEN_SIZE)
        pass

    def unload(self):
        self.logo = None
        pass

    def update(self, total_time: float, frame_time: float):
        if total_time < 1000:
            self.logo.set_opacity(int(total_time // 4))
        elif total_time < 2000:
            self.logo.set_opacity(255)
        elif total_time < 3000:
            self.logo.set_opacity(int((3000-total_time) // 4))
        else:
            self.logo.set_opacity(0)

    def draw(self, screen):
        screen.fill([0,0,0])
        self.logo.draw(screen)
        pass
