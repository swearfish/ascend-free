from engine import FileSystem
from foundation.gcom import Component, auto_gcom


@auto_gcom
class Language(Component):
    file_system: FileSystem

    def __init__(self):
        super().__init__()
        self._static_text_dict = {}
        self._static_text_array = []
        self.history = {}
        self._parse_static_txt()
        self._parse_history_txt()
        self.race_description = self.file_system.read_lines('newgame.txt')

    def _parse_static_txt(self):
        static_txt = self.file_system.read_lines('static.txt')
        file_name = ""
        line_number = 0
        for line in static_txt:
            line = line.strip()
            if 0 == len(line):
                continue
            if line.startswith('//'):
                indexer = line[2:].strip()
                if indexer.isnumeric():
                    line_number = int(indexer)
                elif '-' in indexer:
                    parts = indexer.split('-')
                    if 2 == len(parts) and parts[0].strip().isnumeric():
                        line_number = int(parts[0].strip())
                else:
                    file_name = indexer
            else:
                if line.startswith('"'):
                    end_index = line.find('"', 1)
                    text = line[1:end_index]
                else:
                    text = line
                if file_name not in self._static_text_dict:
                    self._static_text_dict[file_name] = {}
                text = text.replace('\\n', '\n')
                self._static_text_dict[file_name][line_number] = text
                line_number += 1
                self._static_text_array.append(text)

    def _parse_history_txt(self):
        history_txt = self.file_system.read_lines('history.txt')
        species_history = {}
        mode = ''
        for line in history_txt:
            if line.startswith('//') or line=="":
                continue
            if line.startswith('specnum'):
                specnum = int(line[7:].strip())
                species_history = {}
                self.history[specnum] = species_history
            if line.startswith('power') or line.startswith('intro') or line.startswith('text'):
                mode = line
            elif line.startswith('endpower') or line.startswith('endintro') or line.startswith('endtext'):
                mode = ""
            elif mode != '':
                if mode not in species_history:
                    species_history[mode] = [line]
                else:
                    species_history[mode].append(line)

    def get_static(self, file_name: str | None, index: int, *args):
        if file_name is None:
            raw = self._static_text_array[index]
        else:
            raw = self._static_text_dict[file_name][index]
        return self._replace(raw, *args)

    @staticmethod
    def _replace(text: str, *args) -> str:
        arg_value_index = 0
        index = 0
        result = text
        text_arg_index = result.find('%', index)
        while 0 <= text_arg_index:
            arg = result[text_arg_index:text_arg_index+2]
            result = result.replace(arg, str(args[arg_value_index]), 1)
            text_arg_index = result.find('%', index)
            arg_value_index += 1
        return result
