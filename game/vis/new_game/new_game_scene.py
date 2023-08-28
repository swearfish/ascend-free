from foundation.area import area_from_rect
from game.logic.star_map import StarMap
from game.vis.ascendancy_scene import AscendancyScene
from game.vis.star_map_renderer import StarMapRenderer


class NewGameScene(AscendancyScene):
    def __init__(self):
        super().__init__(state_index=3, template_file="data/3cfgnew.tmp")
        self.star_map = StarMap()
        self.star_map_renderer = StarMapRenderer(self.state_frame,
                                                 area_from_rect(7, 7, 300, 300),
                                                 self.star_map)

    def draw(self):
        super().draw()
