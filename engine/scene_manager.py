from typing import Type

from pygame import Surface

from foundation.gcom import Component, auto_gcom
from .abstract_scene import AbstractScene
from .resource_manager import ResourceManager


@auto_gcom
class SceneManager(Component):
    _resource_manager: ResourceManager
    _screen: Surface

    def __init__(self):
        super().__init__()
        self._active_scene: AbstractScene | None = None
        self._scene_time = 0
        self._total_time = 0
        self._next_scene = None
        self._use_history = False
        self._scenes: dict[str, Type[AbstractScene]] = {}
        self._history: list[AbstractScene] = []

    def register_scene(self, name: str, clazz: Type[AbstractScene]):
        self._scenes[name] = clazz

    def enter_scene(self, scene: AbstractScene | Type[AbstractScene] | str):
        if isinstance(scene, str):
            assert scene in self._scenes, f'Unknown scene {scene}'
            scene = self._scenes[scene]
        # noinspection PyTypeChecker
        if isinstance(scene, Type):
            scene = scene()
        if self._active_scene == scene or self._next_scene == scene:
            return
        self._next_scene = scene

    def _do_scene_switch(self):
        if self._active_scene == self._next_scene:
            return
        if self._active_scene is not None:
            self._active_scene.exit()
            if self._use_history:
                if self._active_scene.use_history():
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
            should_handle = self._active_scene.handle_back_key()
        else:
            should_handle = True
        if should_handle and 0 < len(self._history):
            self._next_scene = self._history[-1]
            self._history.pop()
            self._use_history = False
