import pygame

from foundation.vector_2d import Vec2
from game.vis.ascendancy_scene import AscendancyScene
from settings import SCREEN_SIZE


class MainMenu(AscendancyScene):
    def __init__(self):
        super().__init__(state_index=0)
        self.bg = self.resource_manager.load_shape('data/0opening.gif')
        self.buffer = pygame.Surface(SCREEN_SIZE)
        self.click_events['INTRO'] = \
            self.click_events['PLAYTUTORIAL'] = \
            self.click_events['FRESHGAME'] = \
            self.click_events['RESUME'] = \
            self.click_events['LOAD'] = \
            self.click_events['SAVE'] = lambda s, m: self.dialogs.message_box(self.state_frame,
                                                                              s.title,
                                                                              'This function is not yet implemented. '
                                                                              'Please come back later!',
                                                                              'Sure, I will!')
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
        self.bg.draw(self.buffer, Vec2(0, 0))
        self.screen.blit(self.buffer, (0, 0))
        super().draw()

    def handle_back_key(self) -> bool:
        return True
