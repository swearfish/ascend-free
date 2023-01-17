import os.path

import pygame

from ascendancy_assets import convert_voice
from .file_system import FileSystem
from .gcom import gcom


class Jukebox:
    def __init__(self):
        self.fs: FileSystem = gcom.get(FileSystem)
        self.music_list = self.fs.read_lines('music.txt')
        music_count = int(self.music_list[0])
        assert music_count < len(self.music_list)
        self.music_list = self.music_list[1:music_count+1]
        self.playing = False
        self.timeout = 0

    def play_music(self, name: str):
        cached_name = self.fs.get_cached_name(name + '.wav')
        if not os.path.exists(cached_name):
            with self.fs.open_file(name) as voc:
                convert_voice(voc, cached_name)
        pygame.mixer.music.load(cached_name)
        pygame.mixer.music.play()

    def play_now(self, index: int):
        self.play_music(self.music_list[index])
