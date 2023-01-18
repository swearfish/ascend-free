from foundation.ascendancy_exception import AscendancyException


class ShapeException(AscendancyException):
    def __init__(self, msg: str):
        self.msg = msg
