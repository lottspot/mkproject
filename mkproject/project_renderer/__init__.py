
class BaseProjectRenderer():
    def __init__(self, cfg, asset_pack):
        self._cfg = cfg
        self._pack = asset_pack
    def render(self, project):
        raise NotImplementedError()

class MockProjectRenderer(BaseProjectRenderer):
    def render(self, project):
        pack = self._pack
        for path in pack.paths():
            project.register_path(path, pack.data(path))
