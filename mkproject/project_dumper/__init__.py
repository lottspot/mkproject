class BaseProjectDumper():
    def __init__(self, location):
        self._location = location
    def dump(self, project):
        raise NotImplementedError()

class MockProjectDumper(BaseProjectDumper):
    def dump(self, project):
        try:
            self.ncalls += 1
        except AttributeError:
            self.ncalls = 1

class ProjectDumperError(Exception): pass
