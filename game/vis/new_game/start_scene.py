from engine.text.font_manager import FontManager
from engine.text.text_render import TEXT_CENTER, TEXT_VCENTER, TEXT_WRAP
from foundation import Vec2
from foundation.area import area_from_rect
from game.logic.new_game_controller import NewGameController
from game.vis.ascendancy_scene import AscendancyScene
from game.vis.game_fx import GameFx
from game.vis.language import Language


class StartScene(AscendancyScene):

    font_manager: FontManager
    language: Language
    game_fx: GameFx

    def __init__(self):
        # noinspection SpellCheckingInspection
        super().__init__(state_index=12, template_file="data/12start.tmp")

        self.controller = NewGameController()

        species = self.controller.player_species
        self.title = f'{species.name}: {" ".join(species.power)}'
        self.intro = ' '.join(species.intro)
        self.history = ' '.join(species.history)
        self.banner = species.banner_for_color(self.controller.player_color)
        self.face = species.large_face
        self.lg_font = self.font_manager.fonts.get('large')
        self.lg_font_color = self.game_fx.color_large_fonts[self.controller.player_color]

    def draw(self):
        super().draw()

        self.banner.draw(self.screen, Vec2(10, 10))
        self.lg_font_color.text_out(self.title, self.screen, Vec2(320, 22), TEXT_CENTER | TEXT_VCENTER)
        self.face.draw(self.screen, Vec2(7, 46))
        self.lg_font.draw_text(self.intro, self.screen,
                               area_from_rect(330, 60, 620, 220), TEXT_WRAP,
                               line_separator='@')
        self.lg_font_color.draw_text(self.history, self.screen,
                                     area_from_rect(17, 267, 626, 460), TEXT_WRAP,
                                     line_separator='@')
