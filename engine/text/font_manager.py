from ascendancy_assets import Palette, FntFile
from engine import FileSystem
from foundation.gcom import gcom_instance, Component, auto_gcom
from engine.resource_manager import ResourceManager
from engine.text.text_render import TextRenderer


@auto_gcom
class FontManager(Component):
    def __init__(self):
        super().__init__()
        self.fonts: dict[str, TextRenderer] = {}
        self.resource_manager: ResourceManager = gcom_instance.get(ResourceManager)
        self.file_system: FileSystem = gcom_instance.get(FileSystem)

    def register_font(self, name: str, font: str | TextRenderer, palette: Palette = None):
        if isinstance(font, str):
            font = self._load_font(font, palette)
        self.fonts[name] = font
        return font

    def get(self, name: str):
        return self.fonts[name]

    def _load_font(self, name: str, palette: Palette = None) -> TextRenderer:
        from engine.text.bitmap_font import BitmapFont
        from engine.text.bitmap_text_render import BitmapTextRenderer
        if palette is None:
            palette = self.resource_manager.game_pal
        with self.file_system.open_file(name) as f:
            fnt_file = FntFile(name, f, palette)
            bitmap_font = BitmapFont(fnt_file)
            renderer = BitmapTextRenderer(bitmap_font)
            return renderer
