class BaseDumper():
    def __init__(self, location):
        self._location = location
    def __repr__(self):
        return '{}({})'.format(self.__name__, str(self.location))
    def __str__(self):
        return str(self.location)
    @property
    def location(self):
        return self._location
    def dump(self, pack):
        raise NotImplementedError()

class MockDumper(BaseDumper):
    def dump(self, pack):
        try:
            self.ncalls += 1
        except AttributeError:
            self.ncalls = 1

class DumperError(Exception): pass
