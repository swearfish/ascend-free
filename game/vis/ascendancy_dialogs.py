from typing import Optional

from engine.gcom import gcom
from engine.gui.control import Control
from engine.gui.dialog import DialogBuilder, DialogMessageHandler
from engine.resource_manager import ResourceManager
from engine.sprite import ShapeRenderer
from engine.text.font_manager import FontManager
from foundation.area import area_with_size


class AscendancyDialogs:
    def __init__(self):
        self.resource_manager: ResourceManager = gcom.get(ResourceManager)
        self.font_manager: FontManager = gcom.get(FontManager)
        self._dialog_bg = self.resource_manager.load_shape('data/help.shp')
        self._btn_font = self.font_manager.get('large')
        self._txt_font = self.font_manager.get('large')
        self._dialog_button_area = area_with_size(8, 256 - 39, 320, 31)

    def message_box(self, parent: Control, title: str, message: str, ok_button_text='Ok'):
        DialogBuilder(parent) \
            .background(self._dialog_bg) \
            .button_area(self._dialog_button_area) \
            .title(title) \
            .add_button(ok_button_text) \
            .button_font(self._btn_font) \
            .text(message, self._txt_font) \
            .build()

    def question_box(self, parent: Control, message: str, buttons: list[str],
                     listener: DialogMessageHandler,
                     title: Optional[str] = None,
                     shape: ShapeRenderer = None):
        builder = DialogBuilder(parent) \
            .background(self._dialog_bg) \
            .button_area(self._dialog_button_area) \
            .button_font(self._btn_font) \
            .text(message, self._txt_font) \
            .message_handler(listener)
        if title is not None:
            builder.title(title)
        if shape is not None:
            builder.shape(shape)
        for button in buttons:
            builder.add_button(button)
        builder.build()
