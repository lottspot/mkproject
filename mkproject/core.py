from . import assets
from . import project

class Core():
    def __init__(self, loader, dumper, transformer_map={}, cfg={}):
        self._loader = loader
        self._dumper = dumper
        self._transformer_map = transformer_map
        self._cfg = cfg
    def load(self, location):
        pack = assets.load(location, self._loader)
        self._project = pack.transform(self._cfg, self._transformer_map)
    def dump(self, location):
        try:
            proj = self._project
        except AttributeError:
            raise RuntimeError('must call load() before dump()')
        project.dump(location, proj, self._dumper)
    def run(self, load_location, dump_location):
        self.load(load_location)
        self.dump(dump_location)
