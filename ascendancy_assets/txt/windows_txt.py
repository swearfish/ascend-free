# noinspection SpellCheckingInspection

int_attrs = [
    'TYPE',
    'STATENUMBER',
    'STATE',
    'MOUSEFOCUS',
    'X0', 'Y0', 'X1', 'Y1',
    'SHAPEFRAME',
    'SENDMESSAGE', 'SENDPARAM1', 'SENDPARAM2',
    'WINITEMS',
    'NUMCONTROLS',
    'RACE1CONTROL', 'RACE2CONTROL', 'RACE3CONTROL', 'RACE4CONTROL', 'RACE5CONTROL', 'RACE6CONTROL', 'RACE7CONTROL',
]

global_windows = [
    1, 30, 24, 13, 20, 22
]


def parse_windows_txt(lines: str | list[str]) -> dict[str, int | str]:
    if isinstance(lines, str):
        lines = lines.split('\r\n')
    result: dict[str, any] = {
        'tables': [],
        'states': {},
        'global_windows': []
    }
    current_state: dict[str, any] = {}
    current_object: dict[str, any] = result
    for line in lines:
        parts = list(filter(None, line.split(' ')))
        if len(parts) < 2:
            continue
        name: str = parts[0]
        args: list[str | int] = parts[1:]
        if name in int_attrs:
            args = [int(x) for x in args]
        if name == 'TABLE':
            result['tables'].append(args[0])
        if name == 'TYPE':
            type_id: int = args[0]
            if type_id == 100:
                current_state = {
                    'TYPE': type_id,
                    'windows': []
                }
                current_object = current_state
            else:
                current_window = {
                    'TYPE': type_id,
                    'items': []
                }
                current_object = current_window
                if type_id in global_windows:
                    current_window['windows'] = []
                    result['global_windows'].append(current_window)
                    current_state = current_window
                else:
                    current_state['windows'].append(current_window)
        elif name == 'STATENUMBER':
            state_number = args[0]
            current_state[name] = state_number
            result['states'][state_number] = current_state
        elif name.endswith('ITEM'):
            assert len(args) == 5
            args = [int(args[0]), args[1].replace('^', ' '), int(args[2]), int(args[3]), int(args[4])]
            current_object['items'].append((name, args))
        elif len(args) == 1:
            current_object[name] = args[0]
        else:
            current_object[name] = args
    return result
