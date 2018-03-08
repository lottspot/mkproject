from .exceptions import AssetLoaderError

LoaderError = AssetLoaderError

class AssetPack():
    def __init__(self):
        self._pathnames = []
        self._data = {}
        self._meta = {}
    def register_path(self, pathname, data, **meta):
        self._pathnames.append(pathname)
        self._data[pathname] = data
        self._meta[pathname] = dict(meta)
    def data(self, path): pass
    def meta(self, path): pass
    def paths(self): pass
    def assets(self): pass

def load(location, loader_class):
    pack = AssetPack()
    loader = loader_class(location)
    loader.load(pack)
    return pack
