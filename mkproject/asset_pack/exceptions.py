class NotLoadedError(Exception):
    def __init__(self, location):
        self.args = ('resource not loaded: {}'.format(location),)
