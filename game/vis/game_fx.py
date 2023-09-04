from pygame import Surface

from engine.resource_manager import ResourceManager
from engine.text.font_manager import FontManager
from foundation import Vec2
from foundation.gcom import auto_gcom, Component
from game.logic.new_game_controller import Species


@auto_gcom
class GameFx(Component):

    font_manager: FontManager
    resource_manager: ResourceManager
    
    def __init__(self):
        super().__init__()
        self.large_font = self.font_manager.get('large')
        self.small_font = self.font_manager.get('small')
        self.color_large_fonts = []
        self.color_small_fonts = []
        for i in range(0, 8):
            self.color_large_fonts.append(self.font_manager.get(f'large/color={i}'))
            self.color_small_fonts.append(self.font_manager.get(f'small/color={i}'))
        self.race_ring = self.resource_manager.shape_from_file('data/racering.shp')
        self.small_home = self.resource_manager.shape_from_file('data/smhome.shp')

    def draw_player_ring(self, surface: Surface, pos: Vec2, species: Species, color=7):
        species.small_face.draw(surface, pos + Vec2(8, 4), center=False)
        self.race_ring.draw(surface, pos + Vec2(4, 2), index=color)
