from ascendancy_assets.txt.windows_txt import parse_windows_txt
from engine import FileSystem
from engine.gui.button import Button
from engine.gui.state_frame import StateFrame
from engine.resource_manager import ResourceManager
from engine.text.font_manager import FontManager
from foundation.area import area_from_rect
from foundation.gcom import auto_gcom, Component
from foundation.vector_2d import Vec2


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
        self.small_font = self.font_manager.register_font('small', self.windows_txt['SMALLFONT'])
        self.large_font = self.font_manager.register_font('large', self.windows_txt['LARGEFONT'])
        self.states: dict[int, StateFrame] = {}

    def build(self):
        for state_number, state_props in self.windows_txt['states'].items():
            shape_name = state_props['SHAPEFILE']
            shape_frame = state_props['SHAPEFRAME'] if 'SHAPEFRAME' in state_props else 0
            state_frame = StateFrame(state_number, shape_name, shape_frame, self.screen_size)
            self.states[state_number] = state_frame
            for wnd in state_props['windows']:
                if wnd['TYPE'] == 0:
                    # assert wnd['MOUSEFOCUS'] == '1'
                    name = wnd['NAME']
                    x0 = wnd['X0']
                    y0 = wnd['Y0']
                    x1 = wnd['X1']
                    y1 = wnd['Y1']
                    help_index = wnd['HELPINDEX']
                    msg = (wnd['SENDMESSAGE'], wnd['SENDPARAM1'], wnd['SENDPARAM2'])
                    focus = wnd['MOUSEFOCUS'] == 1
                    button = Button(state_frame, name, area_from_rect(x0, y0, x1, y1), help_index, msg, focus)
                    state_frame.controls[name] = button
                    for item_type, item_args in wnd['items']:
                        if item_type == 'TEXTITEM':
                            unused, text, flags, x, y = item_args
                            button.add_text_item(font=self.large_font, text=text.replace('^', ' '),
                                                 pos=Vec2(x, y), flags=flags)

                        if item_type == 'SHAPEITEM':
                            frame, shape, flags, x, y = item_args
                            button.add_shape_item(frame, shape, pos=Vec2(x, y), flags=flags)
