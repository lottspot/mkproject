class BaseDumper():
    def __init__(self, location):
        self._location = location
    def dump(self, pack):
        raise NotImplementedError()

class MockDumper(BaseDumper):
    def dump(self, pack):
        try:
            self.ncalls += 1
        except AttributeError:
            self.ncalls = 1

class DumperError(Exception): pass
