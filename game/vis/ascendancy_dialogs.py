from typing import Optional

from foundation.gcom import gcom_instance
from engine.gui.button import Button
from engine.gui.control import Control
from engine.gui.dialog import DialogBuilder, DialogMessageHandler
from engine.gui.ui_event_listener import UiEventListener
from engine.resource_manager import ResourceManager
from engine.sound_manager import SoundManager
from engine.sprite import ShapeRenderer
from engine.text.font_manager import FontManager
from foundation.area import area_with_size


class AscendancyDialogs(UiEventListener):
    def __init__(self):
        self.resource_manager: ResourceManager = gcom_instance.get(ResourceManager)
        self.font_manager: FontManager = gcom_instance.get(FontManager)
        self.sound_manager: SoundManager = gcom_instance.get(SoundManager)
        self._dialog_bg = self.resource_manager.load_shape('data/help.shp')
        self._btn_font = self.font_manager.get('large')
        self._txt_font = self.font_manager.get('large')
        self._dialog_button_area = area_with_size(8, 256 - 39, 320, 31)

    def message_box(self, parent: Control, title: str, message: str, ok_button_text='Ok'):
        dlg = DialogBuilder(parent) \
            .background(self._dialog_bg) \
            .button_area(self._dialog_button_area) \
            .title(title, title_height=48) \
            .add_button(ok_button_text) \
            .button_font(self._btn_font) \
            .text(message, self._txt_font, border=24) \
            .allow_resize() \
            .build()
        dlg.listener = self

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
        dlg = builder.build()
        dlg.listener = self

    def on_click(self, sender, message) -> bool:
        if isinstance(sender, Button):
            self.sound_manager.play('button')
            return True