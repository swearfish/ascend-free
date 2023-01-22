class AbstractScene:
    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, total_time: float, frame_time: float):
        pass

    def draw(self):
        pass

    def handle_back_key(self) -> bool:
        return False
