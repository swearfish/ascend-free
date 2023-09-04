from foundation.gcom import auto_wire
from game.game_const import STAR_DENSITY, MIN_PLAYERS, MAX_PLAYERS, NUM_SPECIES
from game.logic.new_game_data_model import NewGameDataModel
from game.logic.species import Species
from game.logic.starmap import StarMap
from game.vis.language import Language

STATUS_CPP = 'status.cpp'


@auto_wire
class NewGameController:
    language: Language

    def __init__(self):
        self.event_handler = None

        self.data_model = NewGameDataModel()

        self._star_density_idx = 2
        self._star_density_text = ""

        self._star_densities = STAR_DENSITY
        self._min_species = MIN_PLAYERS
        self._max_species = MAX_PLAYERS

        self.star_map = StarMap(10)

        self._update_star_density()

        self.species = [Species(x) for x in range(0, NUM_SPECIES)]

    def _on_update(self):
        if self.event_handler:
            self.event_handler(self)

    def next_star_density(self):
        self._star_density_idx += 1
        if len(self._star_densities) <= self._star_density_idx:
            self._star_density_idx = 0
        self._update_star_density()
        self._on_update()

    def _update_star_density(self):
        self._star_density_text = self.language.get_static(STATUS_CPP, 155 + self._star_density_idx)
        self.data_model.num_stars = self._star_densities[self._star_density_idx]
        self.star_map.generate_cluster(self.data_model.num_stars)

    def next_species(self):
        self.data_model.num_species += 1
        if self._max_species < self.data_model.num_species:
            self.data_model.num_species = self._min_species
        self._on_update()

    def next_atmosphere(self):
        self.data_model.atmosphere += 1
        if 3 <= self.data_model.atmosphere:
            self.data_model.atmosphere = 0
        self._on_update()

    @property
    def setting_text(self):
        number = self.language.get_static(STATUS_CPP, 163 + self.num_species - self._min_species)
        difficulty = self.language.get_static(STATUS_CPP, 160 + self.data_model.atmosphere)
        return self.language.get_static(STATUS_CPP, 168, self._star_density_text, number, difficulty)

    @property
    def player_species_text(self):
        return self.language.get_static(STATUS_CPP, 153)

    @property
    def star_density(self):
        return self._star_density_idx

    @property
    def num_species(self):
        return self.data_model.num_species

    @property
    def atmosphere(self):
        return self.data_model.atmosphere

    @property
    def player_species(self):
        return self.species[self.data_model.player_species]

    @player_species.setter
    def player_species(self, value):
        if isinstance(value, Species):
            self.data_model.player_species = value.index
        else:
            self.data_model.player_species = value
        self._on_update()

    @property
    def player_color(self):
        return self.data_model.player_color

    @player_color.setter
    def player_color(self, value):
        self.data_model.player_color = value
        self._on_update()
