import typing


class GlobalComponentObjectModel:
    def __init__(self):
        self.instances = {}

    def register(self, clazz, instance=None, init_args=None):
        if instance is None:
            if init_args is None:
                instance = clazz()
            else:
                instance = clazz(*init_args)
        self.instances[self._key_from_class(clazz)] = instance
        return instance

    def get(self, clazz):
        key = self._key_from_class(clazz)
        assert key in self.instances, f'Unknown GCOM: {key}'
        return self.instances[key]

    def has(self, clazz):
        key = self._key_from_class(clazz)
        return key in self.instances

    @staticmethod
    def _key_from_class(clazz):
        return str(clazz)


class Component:
    pass


gcom_instance: GlobalComponentObjectModel = GlobalComponentObjectModel()


def component_resolve(clazz):

    orig_init = clazz.__init__

    # Make copy of original __init__, so we can call it without recursion

    def __init__(self, *args, **kws):
        hint = typing.get_type_hints(clazz)
        for name, member_type in hint.items():
            instance_found = gcom_instance.has(member_type)
            if issubclass(member_type, Component):
                assert instance_found, f"GCOM dependency {member_type} can't be satisfied"
            if instance_found:
                inst = gcom_instance.get(member_type)
                setattr(self, name, inst)
        orig_init(self, *args, **kws)  # Call the original __init__

    clazz.__init__ = __init__  # Set the class' __init__ to the new one
    return clazz
