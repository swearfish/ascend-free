from typing import Optional, Callable

import pygame.draw
from pygame import Surface

from foundation.area import Area, area_with_size, area_from_rect, area_with_size_vec
from foundation.ascendancy_exception import AscendancyException
from foundation.vector import Vec2
from settings import SCREEN_SIZE
from .button import Button
from .control import Control
from .label import Label
from .picture_box import PictureBox
from .ui_event_listener import UiEventListener
from ..sprite import ShapeRenderer
from ..text.text_render import TextRenderer, TEXT_VCENTER, TEXT_CENTER


DialogMessageHandler = Callable[[Control, Control, any], None]


class DialogEventListener(UiEventListener):
    def __init__(self, message_handler: Optional[DialogMessageHandler] = None):
        self._message_handler: Optional[DialogMessageHandler] = message_handler

    def on_click(self, sender, message) -> bool:
        if isinstance(sender, Button):
            self.on_dialog_button_click(sender.parent, sender, message)
            return True

    def on_dialog_button_click(self, dialog, button, message):
        if self._message_handler is not None:
            self._message_handler(dialog, button, message)
        dialog.close()


class DialogBuilder:
    def __init__(self, parent: Control, name: str = "dlg", pos: Optional[Vec2] = None):
        self._parent = parent
        self._name = name

        self._buttons = []
        self._button_area: Area | None = None
        self._button_font: TextRenderer | None = None

        self._background: ShapeRenderer | None = None

        self._shape: ShapeRenderer | None = None
        self._shape_pos: Vec2 | None = None

        self._text: str | None = None
        self._font: TextRenderer | None = None
        self._text_flags = 0

        self._title: str | None = None
        self._title_font: TextRenderer | None = None
        self._title_height = 30

        self._text_border: int = 10

        self._lambda: Optional[DialogMessageHandler] = None

        self._pos = pos

    def background(self, shape: ShapeRenderer):
        self._background = shape
        return self

    def title(self, title: str, font: TextRenderer = None, title_height=30):
        self._title = title
        if font is not None:
            self._title_font = font
        self._title_height = title_height
        return self

    def button_area(self, area: Area):
        self._button_area = area
        return self

    def button_font(self, font: TextRenderer):
        self._button_font = font
        return self

    def add_button(self, title: str, name: str | None = None, msg=None):
        self._buttons.append((title, name, msg))
        return self

    def shape(self, shape: ShapeRenderer, border=10):
        self._shape = shape
        self._shape_pos = Vec2(border, border)
        return self

    def text(self, text: str, font: TextRenderer, flags=0, border=10):
        self._text = text
        self._text_flags = flags
        self._font = font
        self._text_border = border
        return self

    def message_handler(self, message_handler: DialogMessageHandler):
        self._lambda = message_handler
        return self

    def build(self, modal=True, visible=True):
        self._validate()

        area, text_area = self._get_area()
        result = Dialog(self._parent, area, self._name)
        result.listener = DialogEventListener(self._lambda)

        self._get_fonts()
        self._add_background(result)
        self._add_title_bar(result, text_area)
        self._add_image(result, text_area)
        self._add_text(result, text_area)
        self._add_buttons(result)

        result.visible = visible
        if modal:
            if not visible:
                raise AscendancyException("Can't show an invisible modal dialog!")
            self._parent.show_modal(result)

        return result

    def _validate(self):
        assert self._button_area is not None
        assert self._font is not None
        assert self._text is not None
        assert self._background is not None

    def _get_area(self):
        dlg_size = self._background.size
        if self._pos is None:
            screen_center = Vec2(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
            self._pos = screen_center - dlg_size / 2
        area = area_with_size_vec(self._pos, dlg_size)
        text_area = area_from_rect(self._text_border,
                                   self._text_border,
                                   area.width - self._text_border * 2,
                                   self._button_area.top - self._text_border)
        return area, text_area

    def _add_background(self, result):
        PictureBox(result, result.area.new_origin(), self._background)

    def _get_fonts(self):
        if self.button_font is None:
            self._button_font = self._font
        if self._title_font is None:
            self._title_font = self._font

    def _add_title_bar(self, result, text_area):
        if self._title is not None:
            title_area = area_with_size_vec(text_area.top_left, Vec2(text_area.width, self._title_height))
            text_area.top_left.y += self._title_height
            text_area.size.y -= self._title_height
            Label(result, title_area, self._title, self._title_font, TEXT_CENTER | TEXT_VCENTER)

    def _add_image(self, result, text_area):
        if self._shape is not None:
            PictureBox(result, area_with_size_vec(self._shape_pos, self._shape.size), self._shape)
            text_area.top_left.y += self._shape.size.y + self._text_border
            text_area.size.y -= self._shape.size.y + self._text_border

    def _add_text(self, result, text_area):
        if self._text is not None:
            Label(result, text_area, self._text, self._font, self._text_flags, line_spacing=4)

    def _add_buttons(self, result):
        button_left = self._button_area.left
        button_width = self._button_area.width // len(self._buttons)
        button_width_remainder = self._button_area.width - len(self._buttons) * button_width
        mid_button_index = len(self._buttons) // 2
        button_index = 0
        for button_props in self._buttons:
            current_button_width = button_width
            if button_index == mid_button_index:
                current_button_width += button_width_remainder
            self._add_button(button_index, button_left, button_props, current_button_width, result)
            button_index += 1
            button_left += current_button_width

    def _add_button(self, button_index, button_left, button_props, button_width, result):
        area = area_with_size(button_left, self._button_area.top, button_width, self._button_area.height)
        name = f'help_button{button_index}' if button_props[1] is None else button_props[1]
        message = button_index if button_props[2] is None else button_props[2]
        button = Button(result, name, area, message=message)
        button.add_text_item(self._button_font, button_props[0], Vec2(0, 0), TEXT_CENTER | TEXT_VCENTER)


class Dialog(Control):
    def __init__(self, parent: Control, area: Area, name: str = "dlg"):
        super().__init__(parent, area, name)
        self.dimming: Surface = pygame.Surface(parent.area.size.to_tuple())
        self.dimming.fill([0, 0, 0, 128])
        self.dimming.set_alpha(128)

    def on_draw(self, screen: Surface, pos: Vec2):
        screen.blit(self.dimming, (0, 0))
        super().on_draw(screen, pos)
