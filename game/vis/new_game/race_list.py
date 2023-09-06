from pygame import Surface

from engine.gui import UiEventListener
from engine.gui.listbox import ListBox
from foundation import Area, Vec2
from game.logic.new_game_controller import NewGameController
from game.logic.species import Species
from game.vis.ascendancy_control import AscendancyControl


class RaceList(AscendancyControl, UiEventListener):

    def __init__(self, parent, area: Area):
        super().__init__(parent, area)
        self._controller: NewGameController | None = None
        self.lst_species = ListBox(self, area.new_origin(Vec2(0, 0)), small=True,
                                   listener=self)

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value
        if self._controller:
            self.lst_species.items = self.controller.species

    def on_listbox_draw_item(self, listbox, surface: Surface, area: Area, item, _index):
        if listbox == self.lst_species:
            species: Species = item
            self.game_fx.draw_player_ring(surface, area.top_left + Vec2(4, 2), species)

    def on_listbox_select(self, listbox, _item, index):
        if listbox == self.lst_species:
            self.controller.player_species = index
