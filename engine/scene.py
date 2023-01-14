from engine.resource_manager import ResourceManager


class Scene:
    def enter(self):
        pass

    def exit(self):
        pass

    def load(self, res: ResourceManager):
        pass

    def unload(self):
        pass

    def update(self, total_time: float, frame_time: float):
        pass

    def draw(self, screen):
        pass
