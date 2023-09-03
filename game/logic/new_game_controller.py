from engine.resource_manager import ResourceManager
from engine.surface_renderer import SurfaceRenderer
from foundation.gcom import auto_wire
from game.game_const import STAR_DENSITY, DEFAULT_NUM_PLAYERS, MIN_PLAYERS, MAX_PLAYERS, NUM_SPECIES
from game.logic.starmap import StarMap
from game.vis.language import Language

STATUS_CPP = 'status.cpp'


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



@auto_wire
class NewGameController:
    language: Language

    def __init__(self):
        self.event_handler = None

        self._star_density_idx = 0
        self._star_density = ""
        self._num_species = DEFAULT_NUM_PLAYERS
        self._player_color = 0
        self._player_species = 0
        self._atmosphere = 1

        self._star_densities = STAR_DENSITY
        self._min_species = MIN_PLAYERS
        self._max_species = MAX_PLAYERS

        self.star_map = StarMap(10)

        self.next_star_density()
        self.next_star_density()

        self.species = [Species(x) for x in range(0, NUM_SPECIES)]

    def _on_update(self):
        if self.event_handler:
            self.event_handler(self)

    def next_star_density(self):
        self._star_density_idx += 1
        if len(self._star_densities) <= self._star_density_idx:
            self._star_density_idx = 0
        self._star_density = self.language.get_static(STATUS_CPP, 155 + self._star_density_idx)
        num_stars = self._star_densities[self._star_density_idx]
        self.star_map.generate_cluster(num_stars)
        self._on_update()

    def next_species(self):
        self._num_species += 1
        if self._max_species < self._num_species:
            self._num_species = self._min_species
        self._on_update()

    def next_atmosphere(self):
        self._atmosphere += 1
        if 3 <= self._atmosphere:
            self._atmosphere = 0
        self._on_update()

    @property
    def setting_text(self):
        number = self.language.get_static(STATUS_CPP, 163 + self.num_species - self._min_species)
        difficulty = self.language.get_static(STATUS_CPP, 160 + self._atmosphere)
        return self.language.get_static(STATUS_CPP, 168, self._star_density, number, difficulty)

    @property
    def player_species_text(self):
        return self.language.get_static(STATUS_CPP, 153)

    @property
    def star_density(self):
        return self._star_density_idx

    @property
    def num_species(self):
        return self._num_species

    @property
    def atmosphere(self):
        return self._atmosphere
