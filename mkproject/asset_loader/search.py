from . import BaseAssetLoader
from . import AssetLoaderError

class SearchLocation():
    def __init__(self, base):
        self._base = base
        self._loadermap = []
    @property
    def base(self):
        return self._base
    def register_loader(self, tail, loader_class):
        self._loadermap.append((tail, loader_class))
    def get(self):
        try_pairs = []
        for tail, loader_class in self._loadermap:
            try_pairs.append(
                (self.base + tail, loader_class)
            )
        return tuple(try_pairs)

class SearchAssetLoader(BaseAssetLoader):
    def load(self, pack):
        search_paths = self._location.get()
        for path, loader_class in search_paths:
            try:
                loader = loader_class(path)
                return loader.load(pack)
            except AssetLoaderError:
                continue
        raise AssetLoaderError('Failed to load asset pack from {}'.format(location.base))