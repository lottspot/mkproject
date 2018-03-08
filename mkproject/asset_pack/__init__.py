from mkproject.asset_pack.exceptions import NotLoadedError

class BaseAssetPack():
    def __init__(self, location):
        self.location = location
    def __repr__(self):
        return 'BaseAssetPack({})'.format(str(self.location))
    def __str__(self):
        return str(self.location)
    @property
    def assets(self):
        try:
            return self._assets
        except AttributeError:
            raise NotLoadedError(self.location)
    @property
    def metadata(self):
        try:
            return self._metadata
        except AttributeError:
            raise NotLoadedError(self.location)
    def load(self, path):
        # Method must be implemented by concrete asset pack types
        raise NotImplementedError()

class MockAssetPack(BaseAssetPack):
    def __repr__(self):
        return 'MockAssetPack({})'.format(str(self.location))
    def load(self):
        self._assets = {
            'some/file' : r'raw file bytes'.encode(),
            'some/other/file' : r'more file bytes'.encode()
        }
        self._metadata = {
            'some/file': { 'type': 'template' },
            'some/other/file': { 'type': 'static' }
        }
