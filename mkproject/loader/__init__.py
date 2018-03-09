class BaseLoader():
    def __init__(self, location):
        self._location = location
    def __repr__(self):
        return '{}({})'.format(self.__name__, str(self._location))
    def __str__(self):
        return str(self._location)
    def load(self, pack):
        raise NotImplementedError()

class MockLoader(BaseLoader):
    def load(self, pack):
        try:
            self.ncalls += 1
        except AttributeError:
            self.ncalls = 1

class LoaderError(Exception): pass
