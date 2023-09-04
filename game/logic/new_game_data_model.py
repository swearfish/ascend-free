from game.game_const import DEFAULT_NUM_PLAYERS


class NewGameDataModel:
    def __init__(self):
        self.num_stars = 50
        self.num_species = DEFAULT_NUM_PLAYERS
        self.player_color = 0
        self.player_species = 0
        self.atmosphere = 1
