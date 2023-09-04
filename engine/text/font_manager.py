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
        self.registry: dict[str, str] = {}
        self.resource_manager: ResourceManager = gcom_instance.get(ResourceManager)
        self.file_system: FileSystem = gcom_instance.get(FileSystem)

    def register_font(self, name: str, font: str | TextRenderer, palette: Palette = None, palette_shift=0):
        if isinstance(font, str):
            self.registry[name] = font
            font = self._load_font(font, palette, palette_shift)
        self.fonts[name] = font
        return font

    def exists(self, name: str) -> bool:
        return name in self.fonts

    def get(self, name: str) -> TextRenderer:
        return self.fonts[name]

    def _load_font(self, name: str, palette: Palette = None, palette_shift=0) -> TextRenderer:
        from engine.text.bitmap_font import BitmapFont
        from engine.text.bitmap_text_render import BitmapTextRenderer
        if palette is None:
            palette = self.resource_manager.game_pal
        with self.file_system.open_file(name) as f:
            fnt_file = FntFile(name, f, palette, palette_shift)
            bitmap_font = BitmapFont(fnt_file, palette_shift=palette_shift)
            renderer = BitmapTextRenderer(bitmap_font)
            return renderer
