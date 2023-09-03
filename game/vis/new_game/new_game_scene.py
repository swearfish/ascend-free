from pygame import Surface

from engine.gui import Button
from engine.gui.listbox import ListBox
from engine.text.font_manager import FontManager
from engine.text.text_render import TEXT_CENTER, TEXT_VCENTER
from foundation import Vec2
from foundation.area import area_from_rect, area_with_size, Area
from game.game_const import MIN_PLAYERS
from game.logic.new_game_controller import NewGameController, Species
from game.vis.ascendancy_scene import AscendancyScene
from game.vis.language import Language
from game.vis.star_map_renderer import StarMapRenderer


class NewGameScene(AscendancyScene):

    font_manager: FontManager
    language: Language

    def __init__(self):
        # noinspection SpellCheckingInspection
        super().__init__(state_index=3, template_file="data/3cfgnew.tmp")

        self.large_font = self.font_manager.get('large')
        self.small_font = self.font_manager.get('small')

        self.btn_galaxy: Button = self.state_frame.controls['GALAXY_MORE']
        self.btn_players: Button = self.state_frame.controls['PLAYERS_MORE']
        self.btn_atmosphere: Button = self.state_frame.controls['DIFFICULTYMORE']

        self.btn_player_color = Button(self.state_frame,
                                       "color",
                                       area=area_with_size(378, 381, 116, 92),
                                       mouse_focus=False)
        self.btn_player_color.add_text_item(self.large_font, "Player Color", Vec2(0, 10), TEXT_CENTER)
        self.btn_begin_game = Button(self.state_frame,
                                     'begin',
                                     area=area_with_size(501, 381, 132, 92))
        self.btn_begin_game.add_text_item(self.large_font,
                                          self.language.get_static('status.cpp', 169),
                                          Vec2(0, 70), TEXT_CENTER)

        self.controller = NewGameController()
        self.controller.event_handler = lambda c: self.on_update(c)

        self.lst_species = ListBox(self.state_frame, area_from_rect(503, 44, 632, 372),
                                   small=True, items=self.controller.species)

        self.on_update(self.controller)

        self.star_map_renderer = StarMapRenderer(self.state_frame,
                                                 area_from_rect(7, 7, 300, 300),
                                                 self.controller.star_map)
        self.star_map_renderer.animate = True

        self.btn_begin_sm = StarMapRenderer(self.btn_begin_game,
                                            area_from_rect(7, 7, 60, 60),
                                            self.controller.star_map)
        self.btn_begin_sm.animate = True
        self.btn_begin_sm.scale = 0.2
        self.btn_begin_sm.transparent = True

        self.click_events['GALAXY_MORE'] = lambda s, m: self.controller.next_star_density()
        self.click_events['PLAYERS_MORE'] = lambda s, m: self.controller.next_species()
        self.click_events['DIFFICULTYMORE'] = lambda s, m: self.controller.next_atmosphere()

    def draw(self):
        super().draw()
        self.large_font.draw_text(self.controller.setting_text, self.screen,
                                  area_from_rect(7, 310, 300, 350), TEXT_CENTER)
        self.large_font.text_out(self.controller.player_species_text, self.screen,
                                 Vec2(565, 22), TEXT_CENTER | TEXT_VCENTER)

    def on_update(self, controller: NewGameController):
        self.btn_galaxy.shape_frame = controller.star_density
        self.btn_players.shape_frame = 5 + controller.num_species - MIN_PLAYERS
        self.btn_atmosphere.shape_frame = 10 + controller.atmosphere

    def on_listbox_draw_item(self, listbox, surface: Surface, area: Area, item, index):
        if listbox == self.lst_species:
            species: Species = item
            species.small_face.draw(surface, area.top_left + Vec2(8, 5), center=False)
