from pygame import Surface

from foundation import Area


class UiEventListener:
    def on_click(self, sender, message) -> bool:
        pass

    def on_scroll(self, sender, direction, offset):
        pass

    def on_dialog_button_click(self, dialog, button, message):
        pass

    def on_listbox_select(self, listbox, item, index):
        pass

    def on_listbox_draw_item(self, listbox, surface: Surface, area: Area, item, index):
        pass
