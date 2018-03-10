import copy
from .transformer import transform as default_transform

class AssetPack():
    def __init__(self):
        self._data = {}
        self._meta = {}
    def __repr__(self):
        return '{}{}'.format(self.__name__, str(self.paths()))
    def __str__(self):
        return str(self.paths())
    def register_path(self, path, data, **meta):
        self._data[path] = data
        self._meta[path] = dict(meta)
    def paths(self):
        return tuple(self._data.keys())
    def data(self, path):
        try:
            return copy.deepcopy(self._data[path])
        except KeyError:
            raise AttributeError('Unregistered path: {}'.format(path))
    def meta(self, path):
        try:
            self._data[path]
        except KeyError:
            raise AttributeError('No asset for path: {}'.format(path))
        return dict(self._meta.get(path, {}))
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
        pack = AssetPack()
        for asset in self.assets():
            asset = copy.deepcopy(asset)
            mapnames = asset['meta'].pop('pipeline', [])
            pipeline = []
            for name in mapnames:
                try:
                    step = transformer_map[name]
                    pipeline.append(step)
                except KeyError:
                    raise RuntimeError('failed to transform {}: no transformer: {}'.format(asset['path'], name))
            if len(pipeline) < 1:
                pipeline.append(default_transform)
            path, data, meta = self._transform_pipeline(pipeline, cfg, **asset)
            pack.register_path(path, data, **meta)
        return pack
    def _transform_pipeline(self, pipeline, cfg, path, data, meta):
        transform = pipeline[0]
        if len(pipeline) == 1:
            return transform(cfg, path, data, meta)
        else:
            return self._transform_pipeline(pipeline[1:], cfg, *transform(cfg, path, data, meta))
