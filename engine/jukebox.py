import os.path

import pygame

from ascendancy_assets import convert_voice
from .file_system import FileSystem
from .gcom import gcom
from .sound_manager import SoundManager


class Jukebox:
    def __init__(self):
        self.fs: FileSystem = gcom.get(FileSystem)
        self.sound_manager: SoundManager = gcom.get(SoundManager)
        self.music_list = self.fs.read_lines('music.txt')
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
