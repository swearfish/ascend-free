import pygame

from engine.scene import Scene
from engine.lin_alg import Vec2
from settings import SCREEN_SIZE, ORIGINAL_SCREEN_SIZE, FONT_SIZE


class MainMenu(Scene):
    def __init__(self, sm):
        super().__init__(sm)
        self.bg = self.resource_manager.sprite_from_gif('data/0opening.gif', size=SCREEN_SIZE)
        self.buffer = pygame.Surface(SCREEN_SIZE)
        self.small_font = self.resource_manager.get_font('data/smfont.fnt')
        self.big_font = self.resource_manager.get_font('data/bigfont.fnt')
        self.intro_font = self.resource_manager.get_font('data/intro.fnt')
        self.font_size = FONT_SIZE
        pass

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
        self.small_font.text_out('Hello world', self.screen, Vec2(0, 0), FONT_SIZE)
        self.big_font.text_out('Hello world', self.screen, Vec2(0, 20), FONT_SIZE)
        self.intro_font.text_out('Hello world', self.screen, Vec2(0, 50), FONT_SIZE)
