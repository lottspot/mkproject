class BaseProjectDumper():
    def __init__(self, location):
        self._location = location
    def dump(self, project):
        raise NotImplementedError()

class MockProjectDumper(BaseProjectDumper):
    def dump(self, project): pass
