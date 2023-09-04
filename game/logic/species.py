from engine.resource_manager import ResourceManager
from engine.surface_renderer import SurfaceRenderer
from foundation.gcom import auto_wire
from game.vis.language import Language


@auto_wire
class Species:
    resource_manager: ResourceManager
    language: Language

    def __init__(self, index: int):
        self.name = self.language.get_static('race.cpp', 101 + index)
        self.index = index
        self._large_face = None
        self._small_face = None
        self._description = self.language.race_description[index]
        pass

    @property
    def description(self):
        return self.language.get_static('status.cpp', 154, self.name, self._description)

    @property
    def power(self):
        return self.language.history[self.index]['power']

    @property
    def intro(self):
        return self.language.history[self.index]['intro']

    @property
    def history(self):
        return self.language.history[self.index]['text']

    @property
    def large_face(self) -> SurfaceRenderer:
        if not self._large_face:
            self._large_face = self.resource_manager.renderer_from_shape_or_gif(
                f'data/lgrace{self.index:02}.shp', 0)
        return self._large_face

    @property
    def small_face(self) -> SurfaceRenderer:
        if not self._small_face:
            self._small_face = self.resource_manager.renderer_from_shape_or_gif(
                f'data/smrace{self.index:02}.shp', 0)
            self._small_face.set_color_key()
        return self._small_face

    def banner_for_color(self, color: int):
        return self.resource_manager.renderer_from_shape_or_gif('data/raceflag.shp', self.index,
                                                                palette_shift=color*4)
