from pygame import Surface

from engine.game_engine import the_engine
from engine.resource_manager import ResourceManager


class Scene:
    def __init__(self, scene_manager):
        self.resource_manager: ResourceManager = the_engine.get(ResourceManager)
        self.screen: Surface = the_engine.get(Surface)
        self.scene_manager = scene_manager
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, total_time: float, frame_time: float):
        pass

    def draw(self):
        pass
