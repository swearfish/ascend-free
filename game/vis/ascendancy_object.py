from engine import FileSystem
from engine.gui import Control
from engine.resource_manager import ResourceManager
from engine.text.font_manager import FontManager
from foundation import Area
from foundation.gcom import auto_wire
from game.vis.game_fx import GameFx
from game.vis.language import Language


@auto_wire
class AscendancyObject:

    resource_manager: ResourceManager
    file_system: FileSystem
    game_fx: GameFx
    font_manager: FontManager
    language: Language

    def __init__(self):
        pass
