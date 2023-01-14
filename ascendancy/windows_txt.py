def load_windows_txt(lines: str | list[str]) -> dict[str, int | str]:
    if isinstance(lines, str):
        lines = lines.split('\r\n')
    result = {
        'tables': [],
        'states': {}
    }
    current_state = {}
    current_window = {}
    current_object = result
    for line in lines:
        parts = list(filter(None, line.split(' ')))
        if len(parts) < 2:
            continue
        name = parts[0]
        args = parts[1:]
        if name == 'TABLE':
            result['tables'].append(args[0])
        if name == 'TYPE':
            type = int(args[0])
            if type == 100:
                current_state = {
                    'TYPE': type,
                    'windows': []
                }
                current_object = current_state
            else:
                current_window = {
                    'TYPE': type,
                    'items': []
                }
                current_object = current_window
                current_state['windows'].append(current_window)
        elif name == 'STATENUMBER':
            state_number = int(args[0])
            current_state[name] = state_number
            result['states'][state_number] = current_state
        elif name.endswith('ITEM'):
            current_object['items'].append((name, args))
        elif len(args) == 1:
            current_object[name] = args[0]
        else:
            current_object[name] = args
    return result