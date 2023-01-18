import os

from pygame.mixer import Sound

from ascendancy_assets import convert_voice
from engine import FileSystem
from engine.gcom import gcom
from foundation.ascendancy_exception import AscendancyException


class SoundManager:
    def __init__(self):
        self.fs: FileSystem = gcom.get(FileSystem)
        sfx_txt = self.fs.read_lines('soundfx.txt')
        self.sounds: dict[str, Sound] = {}
        for i in range(len(sfx_txt)):
            if sfx_txt[i].strip() == '':
                num_sounds = int(sfx_txt[i+1])
                self.sound_files = sfx_txt[i+2:i+2+num_sounds]
                break
        else:
            raise AscendancyException('Invalid sound.txt')

    def get_sound(self, name: str) -> Sound:
        if name not in self.sounds:
            cached_file = self.get_wav(f'data/{name}.voc')
            sound = Sound(cached_file)
            self.sounds[name] = sound
        return self.sounds[name]

    def play(self, name: str):
        self.get_sound(name).play()

    def get_wav(self, name: str) -> str:
        cached_name = self.fs.get_cached_name(name + '.wav')
        if not os.path.exists(cached_name):
            with self.fs.open_file(name) as voc:
                convert_voice(voc, cached_name)
        return cached_name
