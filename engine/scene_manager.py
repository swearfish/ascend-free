from .game_engine import the_engine
from .resource_manager import ResourceManager
from .scene import Scene


class SceneManager:
    def __init__(self, screen):
        self._active_scene: Scene | None = None
        self._resource_manager: ResourceManager = the_engine.get(ResourceManager)
        self._scene_time = 0
        self._total_time = 0
        self._next_scene = None
        self._screen = screen

    def enter_scene(self, scene: Scene):
        if self._active_scene == scene:
            return
        self._next_scene = scene

    def _do_scene_switch(self):
        if self._active_scene is not None:
            self._active_scene.exit()
            self._active_scene.unload()
        self._active_scene = self._next_scene
        self._next_scene = None
        self._active_scene.load(self._resource_manager)
        self._active_scene.enter()
        self._scene_time = 0

    def update(self, time_delta):
        if self._next_scene is not None:
            self._do_scene_switch()
        if self._active_scene is not None:
            self._scene_time += time_delta
            self._active_scene.update(self._scene_time, time_delta)

    def draw(self):
        if self._active_scene is not None:
            self._active_scene.draw(self._screen)
