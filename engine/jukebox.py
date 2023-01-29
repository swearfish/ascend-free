import pygame

from foundation.gcom import Component, auto_gcom
from .file_system import FileSystem
from .sound_manager import SoundManager


@auto_gcom
class Jukebox(Component):
    file_system: FileSystem
    sound_manager: SoundManager

    def __init__(self):
        super().__init__()
        self.music_list = self.file_system.read_lines('music.txt')
        music_count = int(self.music_list[0])
        assert music_count < len(self.music_list)
        self.music_list = self.music_list[1:music_count+1]
        self.playing = False
        self.timeout = 0

    def play_music(self, name: str):
        cached_name = self.sound_manager.get_wav(name)
        pygame.mixer.music.load(cached_name)
        pygame.mixer.music.play()

    def play_now(self, index: int):
        self.play_music(self.music_list[index])
