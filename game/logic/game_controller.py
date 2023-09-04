import os

from engine import FileSystem
from foundation.gcom import auto_gcom, Component
from game.logic.new_game_data_model import NewGameDataModel
from game.logic.starmap import StarMap


class GameData:
    def __init__(self):
        self.days = 0


@auto_gcom
class GameController(Component):

    file_system: FileSystem
    save_dir: str

    def __init__(self):
        self.star_map: StarMap | None = None

    def new_game(self, data: NewGameDataModel):
        self.star_map = StarMap(data.num_stars)

    def save_game(self, slot: int = 0):
        save_path = self._path_to_save(slot)
        os.makedirs(save_path, exist_ok=True)

    def load_game(self, slot: int = 0):
        pass

    def _path_to_save(self, slot: int):
        return f'{self.save_dir}/{slot:2}.sav' if 0 < slot else f'{self.save_dir}/resume.gam'
