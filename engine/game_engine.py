class GameEngine:
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
        return self.instances[self._key_from_class(clazz)]

    @staticmethod
    def _key_from_class(clazz):
        return str(clazz)


the_engine: GameEngine = GameEngine()
