from .asset_pack import AssetPack
from .loader import LoaderError as _LoaderError
from .dumper import DumperError as _DumperError
from .transformer import TransformerError as _TransformerError

__version__ = '0.0.0'
__pkg__     = 'mkproject'

LoaderError = _LoaderError
DumperError = _DumperError
TransformerError = _TransformerError

def load(location, loader_class):
    pack = AssetPack()
    loader = loader_class(location)
    loader.load(pack)
    return pack

def dump(location, project, dumper_class):
    dumper = dumper_class(location)
    dumper.dump(project)

class Project():
    def __init__(self, loader, dumper, transformer_map={}, cfg={}):
        self._loader = loader
        self._dumper = dumper
        self._transformer_map = transformer_map
        self._cfg = cfg
    def load(self, location):
        pack = load(location, self._loader)
        self._project = pack.transform(self._cfg, self._transformer_map)
    def dump(self, location):
        try:
            project = self._project
        except AttributeError:
            raise RuntimeError('must call load() before dump()')
        dump(location, project, self._dumper)
    def run(self, load_location, dump_location):
        self.load(load_location)
        self.dump(dump_location)
