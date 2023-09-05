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
from game.vis.new_game.species_listbox import SpeciesListBox
from game.vis.galaxy.cosmos_window import CosmosWindow


class GalaxyScene(AscendancyScene):

    font_manager: FontManager
    language: Language
    game_fx: GameFx

    def __init__(self):
        # noinspection SpellCheckingInspection
        super().__init__(state_index=3, template_file="data/1starmap.tmp")

        self.star_map_renderer = CosmosWindow(self.state_frame,
                                              area_from_rect(7, 7, 300, 300),
                                              self.controller.cosmos_wnd)

    def draw(self):
        super().draw()
