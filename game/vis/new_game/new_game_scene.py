from engine.gui import Button
from engine.text.font_manager import FontManager
from engine.text.text_render import TEXT_CENTER, TEXT_VCENTER, TEXT_WRAP
from foundation import Vec2
from foundation.area import area_from_rect, area_with_size
from game.game_const import MIN_PLAYERS
from game.logic.new_game_controller import NewGameController
from game.vis.ascendancy_scene import AscendancyScene
from game.vis.game_fx import GameFx
from game.vis.language import Language
from game.vis.new_game.begin_game_button import BeginGameButton
from game.vis.new_game.player_color_select import PlayerColorPicker
from game.vis.new_game.race_list import RaceList
from game.vis.galaxy.cosmos_window import CosmosWindow


class NewGameScene(AscendancyScene):

    font_manager: FontManager
    language: Language
    game_fx: GameFx

    def __init__(self):
        # noinspection SpellCheckingInspection
        super().__init__(state_index=3, template_file="data/3cfgnew.tmp")

        self.controller = NewGameController()

        self.btn_galaxy: Button = self.state_frame.controls['GALAXY_MORE']
        self.btn_players: Button = self.state_frame.controls['PLAYERS_MORE']
        self.btn_atmosphere: Button = self.state_frame.controls['DIFFICULTYMORE']
        self.lst_species: RaceList = self.state_frame.controls['RACELIST']

        self.lst_species.controller = self.controller

        self.player_color_picker = PlayerColorPicker(self.state_frame,
                                                     area=area_with_size(378, 381, 116, 92),
                                                     controller=self.controller)

        self.btn_begin_game = BeginGameButton(self.state_frame,
                                              'begin',
                                              area=area_with_size(501, 381, 132, 92),
                                              controller=self.controller)

        self.controller.event_handler = lambda c: self.on_update(c)
        self.on_update(self.controller)

        self.cosmos_wnd = CosmosWindow(self.state_frame,
                                       area_from_rect(7, 7, 300, 300),
                                       self.controller.star_map)
        self.cosmos_wnd.animate = True

        self.btn_galaxy.on_click_handler = lambda s, m: self.controller.next_star_density()
        self.btn_players.on_click_handler = lambda s, m: self.controller.next_species()
        self.btn_atmosphere.on_click_handler = lambda s, m: self.controller.next_atmosphere()
        self.btn_begin_game.on_click_handler = lambda s, m: self.scene_manager.enter_scene('start')

    def draw(self):
        super().draw()
        self.game_fx.large_font.draw_text(self.controller.setting_text, self.screen,
                                          area_from_rect(7, 310, 300, 350), TEXT_CENTER)
        self.game_fx.large_font.text_out(self.controller.player_species_text, self.screen,
                                         Vec2(565, 22), TEXT_CENTER | TEXT_VCENTER)
        self._draw_player_species()

    def _draw_player_species(self):
        species = self.controller.player_species
        lg_font = self.game_fx.color_large_fonts[self.controller.player_color]
        sm_font = self.game_fx.color_small_fonts[self.controller.player_color]
        lg_font.text_out(species.name, self.screen, Vec2(400, 22), TEXT_CENTER | TEXT_VCENTER)
        sm_font.draw_text(species.description, self.screen, area_from_rect(330, 260, 480, 350), TEXT_WRAP)

        self.game_fx.draw_player_ring(self.screen, Vec2(344, 40), species, self.controller.player_color)

        self.game_fx.small_home.draw(self.screen, Vec2(370, 190), index=species.index)
        banner = species.banner_for_color(self.controller.player_color)
        banner.draw(self.screen, Vec2(440, 204))

    def on_update(self, controller: NewGameController):
        self.btn_galaxy.shape_frame = controller.star_density
        self.btn_players.shape_frame = 5 + controller.num_species - MIN_PLAYERS
        self.btn_atmosphere.shape_frame = 10 + controller.atmosphere

    def use_history(self) -> bool:
        return False
