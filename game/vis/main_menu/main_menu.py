import pygame

from foundation.vector_2d import Vec2
from game.vis.ascendancy_scene import AscendancyScene
from settings import SCREEN_SIZE


class MainMenu(AscendancyScene):
    def __init__(self):
        super().__init__(state_index=0)
        self.bg = self.resource_manager.renderer_from_shape_or_gif('data/0opening.gif')
        self.buffer = pygame.Surface(SCREEN_SIZE)
        self.click_events['FRESHGAME'] = lambda s, m: self.scene_manager.enter_scene('new_game')
        self.click_events['INTRO'] = \
            self.click_events['PLAYTUTORIAL'] = \
            self.click_events['RESUME'] = \
            self.click_events['LOAD'] = \
            self.click_events['SAVE'] = lambda s, m: self.dialogs.message_box(self.state_frame,
                                                                              s.title,
                                                                              'This function is not yet implemented. '
                                                                              'Please come back later!'
                                                                              f'@@Button: "{s}"'
                                                                              f'@@Msg: "{m}"',
                                                                              'Sure, I will!')
        self.click_events['EXITTODOS'] = lambda s, m: pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.fade_in = True

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, total_time: float, frame_time: float):
        super().update(total_time, frame_time)
        if total_time < 1000 and self.fade_in:
            self.buffer.set_alpha(int(total_time // 4))
        else:
            self.buffer.set_alpha(255)
            self.fade_in = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.bg.draw(self.buffer, Vec2(0, 0))
        self.screen.blit(self.buffer, (0, 0))
        super().draw()

    def handle_back_key(self) -> bool:
        return True
