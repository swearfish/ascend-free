from engine import Jukebox
from engine.scene import Scene
from foundation.gcom import auto_wire
from foundation.vector_2d import Vec2


@auto_wire
class LogoScene(Scene):
    jukebox: Jukebox

    def __init__(self):
        super().__init__()
        self.logo = self.resource_manager.load_shape('data/logo.gif')

    def enter(self):
        pass

    def exit(self):
        self.jukebox.play_now(0)

    def update(self, total_time: float, frame_time: float):
        if total_time < 500:
            self.logo.set_opacity(int(total_time // 2))
        elif total_time < 2000:
            self.logo.set_opacity(255)
        elif total_time < 3000:
            self.logo.set_opacity(int((3000 - total_time) // 4))
        else:
            self.leave()
            self.logo.set_opacity(0)

    def leave(self):
        self.scene_manager.enter_scene('main_menu')

    def draw(self):
        self.screen.fill([0, 0, 0])
        self.logo.draw(self.screen, Vec2(0,0))

    def handle_back_key(self) -> bool:
        self.scene_manager.enter_scene('main_menu')
        return True
