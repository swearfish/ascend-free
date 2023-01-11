import pygame as pg
from pygame.surface import SurfaceType

from .scene import Scene
from .resource_manager import ResourceManager


class SceneManager:
    def __init__(self, first_scene: Scene, screen: pg.Surface | SurfaceType, res: ResourceManager):
        self.active_scene: Scene | None = None
        self.clock = pg.time.Clock()
        self.scene_enter_time = self.clock.get_time()
        self.prev_frame_time = self.clock.get_time()
        self.screen = screen
        self.res = res
        self.enter_scene(first_scene)

    def enter_scene(self, scene: Scene):
        if self.active_scene == scene:
            return
        if self.active_scene is not None:
            self.active_scene.exit()
            self.active_scene.unload()
        self.active_scene = scene
        self.active_scene.load(self.res)
        self.active_scene.enter()

    def update(self):
        time = self.clock.get_time()
        time_scene = time - self.scene_enter_time
        time_elapsed = time - self.prev_frame_time
        self.prev_frame_time = time
        self.active_scene.update(time_scene, time_elapsed)
        self.clock.tick()

    def draw(self):
        self.active_scene.draw(self.screen)
        pg.display.flip()

