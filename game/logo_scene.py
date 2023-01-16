from engine import Jukebox
from engine.game_engine import the_engine
from engine.scene import Scene


class LogoScene(Scene):
    def __init__(self, sm):
        super().__init__(sm)
        self.logo = self.resource_manager.sprite_from_gif('data/logo.gif')
        self.jukebox = the_engine.get(Jukebox)

    def enter(self):
        pass

    def exit(self):
        self.jukebox.play_now(0)

    def update(self, total_time: float, frame_time: float):
        if total_time < 1000:
            self.logo.set_opacity(int(total_time // 4))
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
        self.logo.draw(self.screen)

    def handle_back_key(self) -> bool:
        self.scene_manager.enter_scene('main_menu')
        return True
