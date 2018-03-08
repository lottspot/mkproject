class AssetPack():
    def __init__(self, loader=None):
        self.loader = loader
        self._loaded = False
    def load(self):
        if self._loaded:
            return
        else:
            if self.loader is None:
                raise RuntimeError('Must set AssetPack.loader before calling AssetPack.load()')
            self._pathnames = []
            self._data = {}
            self._meta = {}
            self.loader.load(self)
            self._loaded = True
    def unload(self):
        self._loaded = False
    def register_path(self, pathname, data, **meta):
        self._pathnames.append(pathname)
        self._data[pathname] = data
        self._meta[pathname] = dict(meta)
    def data(self, pathname): pass
    def meta(self, pathname): pass
    def pathnames(self): pass
    def paths(self): pass
