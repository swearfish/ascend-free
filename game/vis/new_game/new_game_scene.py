from foundation import Area
from foundation.area import area_from_rect
from game.logic.star_map import StarMap
from game.vis.ascendancy_scene import AscendancyScene
from game.vis.star_map_renderer import StarMapRenderer


class NewGameScene(AscendancyScene):
    def __init__(self):
        super().__init__(state_index=3)
        #self.template = self.resource_manager.sprite_from_shape_file('data/3cfgnew.tmp')
        sm = StarMap()
        #sm_render = StarMapRenderer(self., area_from_rect(20, 20, 100, 100), sm)

    def draw(self):
        #self.template.draw(self.screen)
        pass
