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

def dump(location, pack, dumper_class):
    dumper = dumper_class(location)
    dumper.dump(pack)

class Project():
    def __init__(self, cfg, loader, dumper):
        self._loader = loader
        self._dumper = dumper
        self._cfg = cfg
    def load(self, location):
        self._pack = load(location, self._loader)
    def transform(self, transformer_map):
        try:
            pack = self._pack
        except AttributeError:
            raise RuntimeError('No asset pack loaded')
        self._pack = pack.transform(self._cfg, transformer_map)
    def dump(self, location):
        try:
            pack = self._pack
        except AttributeError:
            raise RuntimeError('No asset pack loaded')
        dump(location, pack, self._dumper)
    def make(self, load_location, dump_location, transformer_map={}):
        self.load(load_location)
        self.transform(transformer_map)
        self.dump(dump_location)
