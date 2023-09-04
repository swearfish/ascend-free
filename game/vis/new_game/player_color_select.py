import pygame.draw
from pygame import Surface

from engine.gui import Control, Button
from engine.gui.colors import COLOR_BUTTON_BG
from engine.text.text_render import TEXT_CENTER
from foundation import Area, Vec2
from foundation.area import area_with_size
from foundation.gcom import auto_wire
from game.game_const import MAX_PLAYERS
from game.logic.new_game_controller import NewGameController
from game.vis.game_fx import GameFx


@auto_wire
class PlayerColorPicker(Control):

    game_fx: GameFx

    def __init__(self, parent, area: Area, controller: NewGameController):
        super().__init__(parent, area)

        self.controller = controller

    def on_draw(self, screen: Surface, pos: Vec2):
        super().on_draw(screen, pos)
        pygame.draw.rect(screen, COLOR_BUTTON_BG, self.area.new_origin(pos).as_tuple())
        self.game_fx.large_font.text_out("Player Color", screen, Vec2(pos.x+self.area.width/2, pos.y+10), TEXT_CENTER)
        species = self.controller.player_species
        for i in range(0, MAX_PLAYERS):
            area = self._area_for_color(i).move_by(pos)
            banner = species.banner_for_color(i)
            banner.draw(screen, area.top_left)
            if i == self.controller.player_color:
                pygame.draw.rect(screen, [255, 255, 255], area.as_tuple(), 1)

    def on_mouse_click(self, mouse_pos: Vec2) -> bool:
        for i in range(0, MAX_PLAYERS):
            area = self._area_for_color(i)
            if area.contains(mouse_pos):
                self.controller.player_color = i
        return False

    @staticmethod
    def _area_for_color(color: int):
        return area_with_size(3 + color * 16, 54, 15, 25)
