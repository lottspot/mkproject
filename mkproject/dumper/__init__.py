class BaseDumper():
    def __init__(self, location):
        self._location = location
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self.location))
    def __str__(self):
        return str(self.location)
    @property
    def location(self):
        return self._location
    def dump(self, pack):
        raise NotImplementedError()

class DumperError(Exception): pass
