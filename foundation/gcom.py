import inspect
import typing


class Component:
    """
    Root class of all GCOM components
    """

    def close(self):
        pass


class GlobalComponentObjectModel:
    """
    GCOM library, rarely used directly
    Use @auto_wire and @auto_gcom instead or subclass Component
    """

    def __init__(self):
        self._instances: dict[str, Component] = {}
        self._inits: dict[str, typing.Callable] = {}
        self._config: dict[str, any] = {}

    def set_config(self, name: str, value):
        """
        Set the configuration parameter that can be resolved later
        :param name: Name of the parameter to set
        :param value: New value of the parameter
        """
        self._config[name] = value

    def get_config(self, name: str, default_value=None):
        """
        Read a parameter or default_value if not defined
        :param name: Name of the parameter
        :param default_value: Default value returned when parameter is undefined
        :return: Value of the existing parameter value or default_value otherwise
        """
        return self._config[name] if name in self._config else default_value

    def register(self, clazz, init_fun: typing.Callable = None, skip_types: list = None):
        """
        Register a GCOM component. Rarely used directly, use @auto_gcom decorator on class instead
        :param clazz:
        Class type object
        :param init_fun: Alternate initializer function. Uses parameter-less __init__ by default.
        :param skip_types: Register will try to init dependencies too. Types in skip_types are not initialized. Used
        to avoid endless loop on circular component references
        """
        assert clazz is not None
        key = self._key_from_class(clazz)
        assert key not in self._instances, f'GCOM already inited: {key}'
        assert key not in self._inits, f'GCOM already registered: {key}'
        skip_types = skip_types + [clazz] if skip_types is not None else [clazz]

        hints = typing.get_type_hints(clazz)
        for name, member_type in hints.items():
            if inspect.isclass(member_type) and issubclass(member_type, Component):
                if member_type not in skip_types:
                    member_key = self._key_from_class(member_type)
                    if member_key not in self._inits:
                        self.register(member_type, skip_types=skip_types)
        if init_fun is None:
            self._inits[key] = clazz
        else:
            self._inits[key] = init_fun

    def register_all(self, classes):
        """
        Register all classes from the classes list
        :param classes: Class objects to be registered
        """
        for clazz in classes:
            self.register(clazz)

    def shutdown(self):
        """
        De-initialize components
        """
        for inst in self._instances.values():
            inst.close()
        self._instances = []

    def get(self, clazz):
        """
        Get an instance to a GCOM component. The component must be registered, but this function will init
        if not yet initialized. All components are singleton.
        :param clazz: Class of the component to get
        :return: Instance of the type Component
        """
        assert issubclass(clazz, Component)
        key = self._key_from_class(clazz)
        if key in self._instances:
            return self._instances[key]
        assert key in self._inits, f'{key} is not a registered GCOM'
        instance = self._inits[key]()
        self._instances[key] = instance
        return instance

    def is_inited(self, clazz) -> bool:
        """
        Check if a component is initialized
        :param clazz: Component class
        :return: True if the component is already inited
        """
        key = self._key_from_class(clazz)
        return key in self._instances

    def is_registered(self, clazz) -> bool:
        """
        Check if a component is registered
        :param clazz: Component class
        :return: True if the component is registered
        """
        key = self._key_from_class(clazz)
        return key in self._inits

    @staticmethod
    def _key_from_class(clazz):
        return str(clazz)


gcom_instance: GlobalComponentObjectModel = GlobalComponentObjectModel()


def auto_gcom(clazz):
    """
    Similar to auto_wire, but also registers the class as a GCOM component.
    Note: clazz must be a subclass of Component
    :param clazz: Class to be initialized and registered
    :return: Class with prepared initializer
    """
    assert inspect.isclass(clazz) and issubclass(clazz, Component), f'{clazz} is not a component'
    gcom_instance.register(clazz)
    return auto_wire(clazz)


def _auto_wire_init(self):
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


def auto_wire(clazz):
    """
    Use to initialize non-GCOM components. Auto-wire will:
    - Add references to all GCOM components in __init__ that you've declared in the class
    - Add GCOM parameters as member variables

    Example:
      gcom_instance.register(SceneManager)
      gcom_instance.set_param('screen_size', Vec2(640, 480))

      @auto_wire
      class MyClass:
        scene_manager: SceneManager
        screen_size: Vec2

      my_inst = MyClass()
      my_inst.scene_manager.draw(my_inst.screen_size)
    :param clazz: The class to be initialized
    :return: The class with prepared initializer
    """
    orig_init = clazz.__init__

    # Make copy of original __init__, so we can call it without recursion

    def __init__(self, *args, **kws):
        _auto_wire_init(self)
        orig_init(self, *args, **kws)  # Call the original __init__

    clazz.__init__ = __init__  # Set the class' __init__ to the new one
    return clazz
