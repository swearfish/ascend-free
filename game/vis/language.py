from engine import FileSystem
from foundation.gcom import Component, auto_gcom


@auto_gcom
class Language(Component):
    file_system: FileSystem

    def __init__(self):
        super().__init__()
        static_txt = self.file_system.read_lines('static.txt')
        self.text_dict = {}
        self.text_array = []
        file_name = ""
        line_number = 0
        for line in static_txt:
            line = line.strip()
            if 0 == len(line): continue
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
                if file_name not in self.text_dict:
                    self.text_dict[file_name] = {}
                self.text_dict[file_name][line_number] = text
                line_number += 1
                self.text_array.append(text)

    def get_text_file(self, file_name: None, index: int, *args):
        if file_name is None:
            raw = self.text_array[index]
        else:
            key = f'{file_name}:{index}'
            raw = self.text_dict[key]
        return self._replace(raw, args)

    @staticmethod
    def _replace(text: str, *args) -> str:
        arg_index = 0
        index = 0
        result = ""
        while 0 <= index < len(text):
            next_arg_index = text.find('%', index)
            if 0 < next_arg_index:
                result += text[index: next_arg_index]
                result += args[arg_index]
                arg_index += 1
                if text[next_arg_index] == 'l':
                    next_arg_index += 3
                else:
                    next_arg_index += 2
            index = next_arg_index
        result = text[index: ]
        return result