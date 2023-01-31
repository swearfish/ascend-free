from game.vis.ascendancy_scene import AscendancyScene


class NewGameScene(AscendancyScene):
    def __init__(self):
        super().__init__()
        self.template = self.resource_manager.sprite_from_shape_file('data/3cfgnew.tmp')

    def draw(self):
        self.template.draw(self.screen)
