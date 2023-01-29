import inspect
import typing


def get_dependencies(clazz) -> dict:
    hint = typing.get_type_hints(clazz)
    result = {}
    for name, member_type in hint.items():
        if issubclass(member_type, Component):
            result[name] = member_type
    return result


class GlobalComponentObjectModel:
    def __init__(self):
        self._instances: dict[str, Component] = {}
        self._inits: dict[str, typing.Callable] = {}
        self._config: dict[str, any] = {}

    def set_config(self, name: str, value):
        self._config[name] = value

    def get_config(self, name: str, default_value=None):
        return self._config[name] if name in self._config else default_value

    def register(self, clazz, init_fun: typing.Callable = None, skip_types: list = None):
        assert clazz is not None
        key = self._key_from_class(clazz)
        assert key not in self._instances, f'GCOM already inited: {key}'
        assert key not in self._inits, f'GCOM already registered: {key}'
        skip_types = skip_types + [clazz] if skip_types is not None else [clazz]

        hints = typing.get_type_hints(clazz)
        for name, member_type in hints.items():
            if member_type not in skip_types and inspect.isclass(member_type) and issubclass(member_type, Component):
                member_key = self._key_from_class(member_type)
                if member_key not in self._inits:
                    self.register(member_type, skip_types=skip_types)
        if init_fun is None:
            self._inits[key] = clazz
        else:
            self._inits[key] = init_fun

    def register_all(self, classes):
        for clazz in classes:
            self.register(clazz)

    def shutdown(self):
        for inst in self._instances.values():
            inst.close()
        self._instances = []

    def get(self, clazz):
        assert issubclass(clazz, Component)
        key = self._key_from_class(clazz)
        if key in self._instances:
            return self._instances[key]
        assert key in self._inits, f'{key} is not a registered GCOM'
        instance = self._inits[key]()
        self._instances[key] = instance
        return instance

    def has(self, clazz):
        key = self._key_from_class(clazz)
        return key in self._instances

    @staticmethod
    def _key_from_class(clazz):
        return str(clazz)


gcom_instance: GlobalComponentObjectModel = GlobalComponentObjectModel()


def auto_gcom(clazz):
    assert inspect.isclass(clazz) and issubclass(clazz, Component), f'{clazz} is not a component'
    gcom_instance.register(clazz)
    return auto_wire(clazz)


def auto_wire(clazz):
    orig_init = clazz.__init__

    # Make copy of original __init__, so we can call it without recursion

    def __init__(self, *args, **kws):
        hint = typing.get_type_hints(self.__class__)
        for name, member_type in hint.items():
            if inspect.isclass(member_type) and issubclass(member_type, Component):
                inst = gcom_instance.get(member_type)
                setattr(self, name, inst)
            else:
                param_name = name.lstrip('_')
                param_value = gcom_instance.get_config(param_name)
                if param_value is not None:
                    setattr(self, name, param_value)
        orig_init(self, *args, **kws)  # Call the original __init__

    clazz.__init__ = __init__  # Set the class' __init__ to the new one
    return clazz


class Component:
    def close(self):
        pass
