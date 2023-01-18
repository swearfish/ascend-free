class GCOM:
    def __init__(self):
        self.instances = {}

    def register(self, clazz, instance = None, init_args = None):
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

    @staticmethod
    def _key_from_class(clazz):
        return str(clazz)


gcom: GCOM = GCOM()
