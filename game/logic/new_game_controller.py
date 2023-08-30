from foundation.gcom import auto_wire
from game.game_const import STAR_DENSITY, NUMBERS, ATMOSPHERE, DEFAULT_SPECIES, MIN_SPECIES, MAX_SPECIES
from game.logic.starmap import StarMap


@auto_wire
class NewGameController:
    def __init__(self):
        self.event_handler = None

        self._star_density_idx = 0
        self._star_density = ""
        self._num_species = DEFAULT_SPECIES
        self._player_color = 0
        self._player_species = 0
        self._atmosphere = 1

        self._star_densities = [(x, STAR_DENSITY[x]) for x in STAR_DENSITY]

        self.star_map = StarMap(10)

        self.next_star_density()
        self.next_star_density()

    def _on_update(self):
        if self.event_handler:
            self.event_handler(self)

    def next_star_density(self):
        self._star_density_idx += 1
        if len(self._star_densities) <= self._star_density_idx:
            self._star_density_idx = 0
        self._star_density = self._star_densities[self._star_density_idx][0]
        num_stars = self._star_densities[self._star_density_idx][1]
        self.star_map.generate_cluster(num_stars)
        self._on_update()

    def next_species(self):
        self._num_species += 1
        if MAX_SPECIES < self._num_species:
            self._num_species = MIN_SPECIES
        self._on_update()

    def next_atmosphere(self):
        self._atmosphere += 1
        if 3 <= self._atmosphere:
            self._atmosphere = 0
        self._on_update()

    @property
    def setting_text(self):
        return (f'{self._star_density} Star Cluster\n'
                f'{NUMBERS[self._num_species]} Species\n'
                f'{ATMOSPHERE[self._atmosphere]} Atmosphere')

    @property
    def star_density(self):
        return self._star_density_idx

    @property
    def num_species(self):
        return self._num_species

    @property
    def atmosphere(self):
        return self._atmosphere