from ..exceptions import AssetLoaderError

LoaderError = AssetLoaderError

class BaseAssetLoader():
    def __init__(self, location):
        self.location = location
    def __repr__(self):
        return '{}({})'.format(self.__name__, str(self.location))
    def __str__(self):
        return str(self.location)
    def load(self, pack):
        raise NotImplementedError()

class MockAssetLoader(BaseAssetLoader):
    def load(self, pack): pass
