from pygame import Surface

from engine.gui import Button
from engine.text.font_manager import FontManager
from engine.text.text_render import TEXT_CENTER
from foundation import Area, Vec2
from foundation.area import area_from_rect, area_with_size
from foundation.gcom import auto_wire
from game.logic.new_game_controller import NewGameController
from game.vis.game_fx import GameFx
from game.vis.language import Language
from game.vis.star_map.cosmos_window import CosmosWindow


@auto_wire
class BeginGameButton(Button):

    font_manager: FontManager
    language: Language
    game_fx: GameFx

    def __init__(self, parent, name: str, area: Area, controller: NewGameController):
        super().__init__(parent, name, area)
        large_font = self.font_manager.get('large')
        text = self.language.get_static('status.cpp', 169)
        self.add_text_item(large_font, text, Vec2(0, 70), TEXT_CENTER)
        self.cosmos_wnd = CosmosWindow(self, area_from_rect(7, 7, 60, 60), controller.star_map)
        self.cosmos_wnd.animate = True
        self.cosmos_wnd.scale = 0.2
        self.cosmos_wnd.transparent = True
        self.controller = controller

    def on_draw(self, screen: Surface, pos: Vec2):
        super().on_draw(screen, pos)
        self.game_fx.draw_player_ring_scaled(screen,
                                             area_with_size(pos.x+67, pos.y + 7, 50, 50),
                                             self.controller.player_species,
                                             self.controller.player_color)
