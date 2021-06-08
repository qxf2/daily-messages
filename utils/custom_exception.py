from builtins import Exception


class RecursionDepthLimitException(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)