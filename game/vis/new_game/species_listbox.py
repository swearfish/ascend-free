from pygame import Surface

from engine.gui import Control, UiEventListener
from engine.gui.listbox import ListBox
from foundation import Area, Vec2
from foundation.gcom import auto_wire
from game.logic.new_game_controller import NewGameController, Species
from game.vis.game_fx import GameFx


@auto_wire
class SpeciesListBox(Control, UiEventListener):

    game_fx: GameFx

    def __init__(self, parent, area: Area, controller: NewGameController):
        super().__init__(parent, area)
        self.controller = controller
        self.lst_species = ListBox(self, area.new_origin(Vec2(0, 0)), small=True,
                                   items=self.controller.species,
                                   listener=self)

    def on_listbox_draw_item(self, listbox, surface: Surface, area: Area, item, _index):
        if listbox == self.lst_species:
            species: Species = item
            self.game_fx.draw_player_ring(surface, area.top_left, species)

    def on_listbox_select(self, listbox, _item, index):
        if listbox == self.lst_species:
            self.controller.player_species = index
