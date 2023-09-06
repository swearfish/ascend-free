from ascendancy_assets.txt.windows_txt import parse_windows_txt
from engine import FileSystem
from engine.gui.button import Button
from engine.gui.state_frame import StateFrame
from engine.resource_manager import ResourceManager
from engine.text.font_manager import FontManager
from foundation.area import area_from_rect
from foundation.gcom import auto_gcom, Component
from foundation.vector_2d import Vec2
from game.vis.new_game.race_list import RaceList

TYPE_BUTTON = 0
TYPE_LIST = 10


# noinspection SpellCheckingInspection
@auto_gcom
class AscendancyGuiBuilder(Component):
    resource_manager: ResourceManager
    font_manager: FontManager
    file_system: FileSystem
    screen_size: Vec2

    def __init__(self):
        super().__init__()
        self.windows_txt = parse_windows_txt(self.file_system.read_lines('windows.txt'))
        self.game_pal = self.resource_manager.game_pal

        small_font_name = self.windows_txt['SMALLFONT']
        large_font_name = self.windows_txt['LARGEFONT']

        self.small_font = self.font_manager.register_font('small', small_font_name)
        self.large_font = self.font_manager.register_font('large', large_font_name)

        for i in range(0, 8):
            self.font_manager.register_font(f'large/color={i}', large_font_name, self.game_pal, -243 + 16 + 3 + i*4)
            self.font_manager.register_font(f'small/color={i}', small_font_name, self.game_pal, -243 + 16 + 3 + i*4)

    def build_frame(self, state_number: int) -> StateFrame | None:
        states = self.windows_txt['states']
        if state_number not in states:
            return None
        state_props: dict = states[state_number]
        shape_name = state_props['SHAPEFILE']
        shape_frame = state_props['SHAPEFRAME'] if 'SHAPEFRAME' in state_props else 0
        state_frame = StateFrame(state_number, shape_name, shape_frame, self.screen_size)
        for wnd in state_props['windows']:
            name = wnd['NAME']
            x0 = wnd['X0']
            y0 = wnd['Y0']
            x1 = wnd['X1']
            y1 = wnd['Y1']
            area = area_from_rect(x0, y0, x1, y1)
            if wnd['TYPE'] == TYPE_BUTTON:
                self._build_button(state_frame, wnd, name, area)
            elif wnd['TYPE'] == TYPE_LIST:
                if name == 'RACELIST':
                    self._build_race_list(state_frame, name, area)
        return state_frame

    def _build_button(self, state_frame, wnd, name, area):
        help_index = wnd['HELPINDEX']
        msg = (wnd['SENDMESSAGE'], wnd['SENDPARAM1'], wnd['SENDPARAM2'])
        focus = wnd['MOUSEFOCUS'] == 1
        button = Button(state_frame, name, area, help_index, msg, focus)
        state_frame.controls[name] = button
        for item_type, item_args in wnd['items']:
            if item_type == 'TEXTITEM':
                unused, text, flags, x, y = item_args
                button.add_text_item(font=self.large_font, text=text.replace('^', ' '),
                                     pos=Vec2(x, y), flags=flags)

            if item_type == 'SHAPEITEM':
                frame, shape, flags, x, y = item_args
                button.add_shape_item(frame, shape, pos=Vec2(x, y), flags=flags)

    def _build_race_list(self, state_frame, name, area):
        race_list = RaceList(state_frame, area)
        state_frame.controls[name] = race_list
