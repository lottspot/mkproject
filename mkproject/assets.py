from .asset_loader import AssetLoaderError as LoaderError
from .project import ProjectScaffold

AssetLoaderError = LoaderError

class AssetPack():
    def __init__(self):
        self._data = {}
        self._meta = {}
    def register_path(self, path, data, **meta):
        self._data[path] = data
        self._meta[path] = dict(meta)
    def data(self, path):
        try:
            return self._data[path]
        except KeyError:
            raise AttributeError('No asset for path: {}'.format(path))
    def meta(self, path):
        try:
            self._data[path]
        except KeyError:
            raise AttributeError('No asset for path: {}'.format(path))
        return self._meta.get(path, {})
    def paths(self):
        return tuple(self._data.keys())
    def assets(self):
        assets = []
        for path in self.paths():
            assets.append({
                'path': path,
                'data': self.data(path),
                'meta': self.meta(path)
            })
        return tuple(assets)
    def transform(self, transformer_map={}, cfg={}):
        proj = ProjectScaffold()
        for asset in self.assets():
            transform = lambda path, data, meta, cfg: (path, data)
            meta = asset['meta']
            try:
                transform = transformer_map[meta['type']]
            except KeyError:
                pass
            path, data = transform(cfg=cfg, **asset)
            proj.register_path(path, data)
        return proj

def load(location, loader_class):
    pack = AssetPack()
    loader = loader_class(location)
    loader.load(pack)
    return pack
