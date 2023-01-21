from typing import Optional, Callable

import pygame.draw
from pygame import Surface

from foundation.area import Area, area_with_size, area_from_rect, area_with_size_vec
from foundation.ascendancy_exception import AscendancyException
from foundation.vector_2d import Vec2
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
    def __init__(self, dialog: Control, message_handler: Optional[DialogMessageHandler] = None):
        self._message_handler: Optional[DialogMessageHandler] = message_handler
        self._dialog = dialog

    def on_click(self, sender, message) -> bool:
        if isinstance(sender, Button):
            self._dialog.listener.on_click(sender, message)
            self.on_dialog_button_click(sender.parent, sender, message)
            return True

    def on_dialog_button_click(self, dialog, button, message):
        if self._message_handler is not None:
            self._message_handler(dialog, button, message)
        else:
            self._dialog.listener.on_dialog_button_click(dialog, button, message)
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
        self._allow_resize = False

        self._text_border: int = 10
        self._line_spacing = 4
        self._line_separator = '@@'

        self._lambda: Optional[DialogMessageHandler] = None

        self._pos = pos

    def background(self, shape: ShapeRenderer):
        self._background = shape
        return self

    def allow_resize(self):
        self._allow_resize = True
        return self

    def title(self, title: str, font: TextRenderer = None, title_height=30):
        self._title = title
        if font is not None:
            self._title_font = font
        self._title_height = title_height
        return self

    def button_area(self, area: Area):
        self._button_area = area.dup()
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
        if self._allow_resize:
            area, text_area = self._resize(area, text_area)
        result = Dialog(self._parent, area, self._name)
        result.listener = DialogEventListener(result, self._lambda)

        self._get_fonts()
        self._add_background(result)
        text_area = self._add_title_bar(result, area, text_area)
        self._add_image(result, text_area)
        self._add_text(result, text_area)
        self._add_buttons(result)

        result.visible = visible
        if modal:
            if not visible:
                raise AscendancyException("Can't show an invisible modal dialog!")
            self._parent.show_modal(result)

        return result

    def _resize(self, area, text_area):
        text_size = self._font.measure_text(self._text, text_area.width, self._line_spacing, self._line_separator)
        if self._title is not None:
            text_size += Vec2(0, self._title_height)
        text_size += Vec2(0, self._text_border)
        height_diff = text_area.height - text_size.y
        if 0 == height_diff:
            return area, text_area
        assert 0 < height_diff
        self._pos += Vec2(0, height_diff // 2)
        new_dlg_size = Vec2(area.width, area.height - height_diff)
        self._button_area = self._button_area.move_by(Vec2(0, -height_diff))
        new_background = pygame.Surface(new_dlg_size.as_tuple())
        center = new_dlg_size.h // 2
        top_area = area_with_size(0, 0, new_dlg_size.w, center)
        bottom_area = area_from_rect(0, area.height - center, new_dlg_size.w - 1, area.height - 2)
        top_part = self._background.surface.subsurface(top_area.as_tuple())
        bottom_part = self._background.surface.subsurface(bottom_area.as_tuple())
        new_background.blit(top_part, (0, 0))
        new_background.blit(bottom_part, (0, top_part.get_height()))
        self._background = ShapeRenderer(new_background)
        return self._get_area()

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

    def _add_title_bar(self, result, area, text_area):
        if self._title is not None:
            title_area = area_with_size(0, 0, area.width, self._title_height)
            text_area = area_with_size(text_area.left, text_area.top + self._title_height,
                                       text_area.width, text_area.height - self._title_height)
            Label(result, title_area, self._title, self._title_font, TEXT_CENTER | TEXT_VCENTER)
        return text_area

    def _add_image(self, result, text_area):
        if self._shape is not None:
            PictureBox(result, area_with_size_vec(self._shape_pos, self._shape.size), self._shape)
            text_area = area_with_size(text_area.left, text_area.top + self._shape.size.h + self._text_border,
                                       text_area.width, text_area.height - self._shape.size.h - self._text_border)
        return text_area

    def _add_text(self, result, text_area):
        if self._text is not None:
            Label(result, text_area, self._text, self._font, self._text_flags, self._line_spacing, self._line_separator)

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
        button.listener = result.listener


class Dialog(Control):
    def __init__(self, parent: Control, area: Area, name: str = "dlg"):
        super().__init__(parent, area, name)
        self.dimming: Surface = pygame.Surface(parent.area.size.as_tuple())
        self.dimming.fill([0, 0, 0, 128])
        self.dimming.set_alpha(128)

    def on_draw(self, screen: Surface, pos: Vec2):
        screen.blit(self.dimming, (0, 0))
        super().on_draw(screen, pos)
