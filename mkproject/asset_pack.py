import copy
from .transformer import transform as default_transform

class AssetPack():
    def __init__(self):
        self._data = {}
        self._meta = {}
    def register_path(self, path, data, **meta):
        self._data[path] = data
        self._meta[path] = dict(meta)
    def paths(self):
        return tuple(self._data.keys())
    def data(self, path):
        try:
            return self._data[path]
        except KeyError:
            raise AttributeError('Unregistered path: {}'.format(path))
    def meta(self, path):
        try:
            self._data[path]
        except KeyError:
            raise AttributeError('No asset for path: {}'.format(path))
        return self._meta.get(path, {})
    def assets(self):
        assets = []
        for path in self.paths():
            assets.append({
                'path': path,
                'data': self.data(path),
                'meta': self.meta(path)
            })
        return tuple(assets)
    def transform(self, cfg={}, transformer_map={}):
        pack = AssetPack()
        for asset in self.assets():
            asset = copy.deepcopy(asset)
            transform = default_transform
            asset_type = asset['meta'].get('type')
            try:
                transform = transformer_map[asset_type]
            except KeyError:
                pass
            path, data, meta = transform(cfg, **asset)
            if meta.get('type') == asset_type and asset_type is not None:
                # Prevent transformation on subsequent transform() calls
                meta.pop('type')
            pack.register_path(path, data, **meta)
        return pack
