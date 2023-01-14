class Control:
    def __init__(self):
        pass

    def mouse_enter(self):
        pass

    def mouse_leave(self):
        pass

    def mouse_click(self, x: int, y, int):
        pass

    def mouse_down(self, button: int, x: int, y, int):
        pass

    def mouse_up(self, button: int, x: int, y, int):
        pass


class Frame(Control):
    def __init__(self):
        super().__init__()


class Button(Control):
    def __init__(self, name: str, help_index: str = None, area):
        super().__init__()
        self.name = name
        self.area = area
        self.help_index = help_index
        self.items = []
        self.hover = False

    def add_text_item(self, text: str, pos):
        item = TextItem(text, pos)
        self.items.append(item)
        return item

    def mouse_enter(self):
        self.hover = True

    def mouse_leave(self):
        self.hover = False

class TextItem(Control):
    def __init__(self, text: str, pos):
        super().__init__()
        self.pos = pos
        self.text = text