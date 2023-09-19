from engine.gui import Button, Control
from engine.text.font_manager import FontManager
from foundation import Vec2
from foundation.area import area_from_rect
from game.vis.ascendancy_scene import AscendancyScene
from game.vis.galaxy.cosmos_window import CosmosWindow
from game.vis.game_fx import GameFx
from game.vis.language import Language


class GalaxyScene(AscendancyScene):

    font_manager: FontManager
    language: Language
    game_fx: GameFx
    cosmos_

    def __init__(self):
        # noinspection SpellCheckingInspection
        super().__init__(state_index=1, template_file="data/1starmap.tmp")

        self.btn_intelligence = Button(self.state_frame, "Species", area_from_rect(474, 286, 632, 316))
        self.btn_intelligence.add_text_item(self.game_fx.large_font, "Species", Vec2(2, 2), 0)
        self.cosmos_wnd: CosmosWindow = self.state_frame.get_child_of_class(CosmosWindow)
        self.cosmos_wnd.zoom = 30

    def draw(self):
        super().draw()
        if self.cosmos_wnd.selected_star is not None:
            self.game_fx.large_font.text_out(self.cosmos_wnd.selected_star.name, self.screen, Vec2(300, 445), 0)
            type_text = self.language.get_star_type_text(self.cosmos_wnd.selected_star.type)
            self.game_fx.small_font.text_out(type_text, self.screen, Vec2(300, 460), 0)

    def on_click(self, sender: Control, message) -> bool:
        if sender.name == 'ROTLEFT':
            self.cosmos_wnd.rot_y -= 1
        if sender.name == 'ROTRIGHT':
            self.cosmos_wnd.rot_y += 1
        return super().on_click(sender, message)
