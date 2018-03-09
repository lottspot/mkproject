
class BaseProjectRenderer():
    def __init__(self, cfg, asset_pack):
        self._cfg = cfg
        self._pack = asset_pack
    def render(self, project):
        raise NotImplementedError()

class MockProjectRenderer(BaseProjectRenderer):
    def render(self, project):
        try:
            self.ncalls += 1
        except AttributeError:
            self.ncalls = 1

class ProjectRendererError(Exception): pass
