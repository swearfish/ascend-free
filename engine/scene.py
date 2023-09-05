from pygame import Surface

from engine.abstract_scene import AbstractScene
from engine.resource_manager import ResourceManager
from engine.scene_manager import SceneManager
from engine.sound_manager import SoundManager
from engine.text.font_manager import FontManager
from foundation.gcom import auto_wire


@auto_wire
class Scene(AbstractScene):
    """
    Scene class with auto-wired basic resources
    """

    resource_manager: ResourceManager
    font_manager: FontManager
    sound_manager: SoundManager
    scene_manager: SceneManager
    screen: Surface

    def __init__(self):
        pass
