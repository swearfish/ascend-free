import pygame

from engine.gui.control import Control
from engine.scene import Scene
from settings import SCREEN_SIZE


class MainMenu(Scene):
    def __init__(self, sm):
        super().__init__(sm, state_index=0)
        self.bg = self.resource_manager.sprite_from_gif('data/0opening.gif')
        self.buffer = pygame.Surface(SCREEN_SIZE)
        self.click_events['EXITTODOS'] = lambda s, m: pygame.event.post(pygame.event.Event(pygame.QUIT))

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, total_time: float, frame_time: float):
        if total_time < 1000:
            self.buffer.set_alpha(int(total_time // 4))
        else:
            self.buffer.set_alpha(255)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.bg.draw(self.buffer)
        self.screen.blit(self.buffer, (0, 0))
        super().draw()

    def handle_back_key(self) -> bool:
        return True
