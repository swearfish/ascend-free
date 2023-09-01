from engine.gui import Button
from engine.text.font_manager import FontManager
from engine.text.text_render import TEXT_CENTER, TEXT_VCENTER
from foundation import Vec2
from foundation.area import area_from_rect
from game.game_const import MIN_SPECIES
from game.logic.new_game_controller import NewGameController
from game.vis.ascendancy_scene import AscendancyScene
from game.vis.star_map_renderer import StarMapRenderer


class NewGameScene(AscendancyScene):

    font_manager: FontManager

    def __init__(self):
        # noinspection SpellCheckingInspection
        super().__init__(state_index=3, template_file="data/3cfgnew.tmp")

        self.btn_galaxy:Button = self.state_frame.controls['GALAXY_MORE']
        self.btn_players:Button = self.state_frame.controls['PLAYERS_MORE']
        self.btn_atmosphere:Button = self.state_frame.controls['DIFFICULTYMORE']

        self.controller = NewGameController()
        self.controller.event_handler = lambda c: self.on_update(c)
        self.on_update(self.controller)
        self.star_map_renderer = StarMapRenderer(self.state_frame,
                                                 area_from_rect(7, 7, 300, 300),
                                                 self.controller.star_map)
        self.star_map_renderer.animate = True
        self.click_events['GALAXY_MORE'] = lambda s,m: self.controller.next_star_density()
        self.click_events['PLAYERS_MORE'] = lambda s,m: self.controller.next_species()
        self.click_events['DIFFICULTYMORE'] = lambda s,m: self.controller.next_atmosphere()

        self.large_font = self.font_manager.get('large')
        self.small_font = self.font_manager.get('small')

    def draw(self):
        super().draw()
        self.large_font.draw_text(self.controller.setting_text, self.screen, area_from_rect(7, 310, 300, 350), TEXT_CENTER)
        self.large_font.text_out(self.controller.player_species_text, self.screen, Vec2(565, 22), TEXT_CENTER | TEXT_VCENTER)

    def on_update(self, controller: NewGameController):
        self.btn_galaxy.shape_frame = controller.star_density
        self.btn_players.shape_frame = 5 + controller.num_species - MIN_SPECIES
        self.btn_atmosphere.shape_frame = 10 + controller.atmosphere
