class BaseDumper():
    def __init__(self, location):
        self._location = location
    def dump(self, project):
        raise NotImplementedError()

class MockDumper(BaseDumper):
    def dump(self, project):
        try:
            self.ncalls += 1
        except AttributeError:
            self.ncalls = 1

class DumperError(Exception): pass
