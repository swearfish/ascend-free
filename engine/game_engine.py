from .file_system import FileSystem
from .resource_manager import ResourceManager
from .scene_manager import SceneManager
from .jukebox import Jukebox


class GameEngine:
    def __init__(self):
        self.file_system: FileSystem | None = None
        self.resource_manager: ResourceManager | None = None
        self.scene_manager: SceneManager | None = None
        self.jukebox: Jukebox | None = None


the_engine: GameEngine = GameEngine()
