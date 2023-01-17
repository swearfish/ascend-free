from typing import Type

from .gcom import gcom
from .resource_manager import ResourceManager
from .scene import Scene


class SceneManager:
    def __init__(self, screen):
        self._active_scene: Scene | None = None
        self._resource_manager: ResourceManager = gcom.get(ResourceManager)
        self._scene_time = 0
        self._total_time = 0
        self._next_scene = None
        self._use_history = False
        self._screen = screen
        self._scenes: dict[str, Type[Scene]] = {}
        self._history: list[Scene] = []

    def register_scene(self, name: str, clazz: Type[Scene]):
        self._scenes[name] = clazz

    def enter_scene(self, scene: Scene | Type[Scene] | str):
        if isinstance(scene, str):
            assert scene in self._scenes, f'Unknown scene {scene}'
            scene = self._scenes[scene]
        # noinspection PyTypeChecker
        if isinstance(scene, Type):
            scene = scene(self)
        if self._active_scene == scene or self._next_scene == scene:
            return
        self._next_scene = scene
        self._use_history = True

    def _do_scene_switch(self):
        if self._active_scene == self._next_scene:
            return
        if self._active_scene is not None:
            self._active_scene.exit()
            if self._use_history:
                self._history.append(self._active_scene)
                self._use_history = False
        self._active_scene = self._next_scene
        self._next_scene = None
        if self._active_scene is not None:
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
            self._active_scene.draw()

    def back_button_press(self):
        if self._active_scene is not None:
            is_handled = self._active_scene.handle_back_key()
        else:
            is_handled = False
        if not is_handled and 0 < len(self._history):
            self._next_scene = self._history[-1]
            self._history.pop()
            self._use_history = False

