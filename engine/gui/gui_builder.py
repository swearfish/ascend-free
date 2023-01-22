from engine.gui.button import Button
from engine.gui.state_frame import StateFrame
from engine.resource_manager import ResourceManager
from engine.text.font_manager import FontManager
from foundation.area import area_from_rect
from foundation.gcom import component_resolve, Component
from foundation.vector_2d import Vec2


# noinspection SpellCheckingInspection
@component_resolve
class AscendancyGui(Component):
    resource_manager: ResourceManager
    font_manager: FontManager

    def __init__(self, windows_txt: dict[str, any], screen_res=Vec2(640, 480)):
        self.game_pal = self.resource_manager.game_pal
        self.small_font = self.font_manager.register_font('small', windows_txt['SMALLFONT'])
        self.large_font = self.font_manager.register_font('large', windows_txt['LARGEFONT'])
        self.states: dict[int, StateFrame] = {}
        for state_number, state_props in windows_txt['states'].items():
            shape_name = state_props['SHAPEFILE']
            state_frame = StateFrame(state_number, shape_name, screen_res)
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
                    button = Button(state_frame, name, area_from_rect(x0, y0, x1, y1), help_index, msg)
                    for item_type, item_args in wnd['items']:
                        if item_type == 'TEXTITEM':
                            unused, text, flags, x, y = item_args
                            button.add_text_item(font=self.large_font, text=text.replace('^', ' '),
                                                 pos=Vec2(x, y), flags=flags)
