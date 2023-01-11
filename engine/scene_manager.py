import pygame as pg
from pygame.surface import SurfaceType

from .scene import Scene
from .resource_manager import ResourceManager


class SceneManager:
    def __init__(self, first_scene: Scene, screen: pg.Surface | SurfaceType, res: ResourceManager):
        self.active_scene: Scene | None = None
        self.clock = pg.time.Clock()
        self.scene_enter_time = pg.time.get_ticks()
        self.screen = screen
        self.res = res
        self.enter_scene(first_scene)
        self.frame_rate = 30

    def enter_scene(self, scene: Scene):
        if self.active_scene == scene:
            return
        if self.active_scene is not None:
            self.active_scene.exit()
            self.active_scene.unload()
        self.active_scene = scene
        self.active_scene.load(self.res)
        self.active_scene.enter()
        self.scene_enter_time = pg.time.get_ticks()

    def update(self):
        self.clock.tick(self.frame_rate)
        current_time = pg.time.get_ticks()
        total_scene_time = current_time - self.scene_enter_time
        time_elapsed = self.clock.get_time()
        self.active_scene.update(total_scene_time, time_elapsed)

    def draw(self):
        self.active_scene.draw(self.screen)
        pg.display.flip()

