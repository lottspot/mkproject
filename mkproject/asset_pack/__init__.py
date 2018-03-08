
class BaseAssetPack():
    assets = None
    metadata = None
    def __init__(self, path):
        self._load_assets(path)
    def _load_assets(self, path):
        # Method must be implemented by concrete asset pack types
        raise NotImplementedError()

class MockAssetPack():
    def __init__(self, location):
        self.location = location
    def __repr__(self):
        return 'MockAssetPack({})'.format(str(self.location))
    def __str__(self):
        return str(self.location)
    def _load_assets(self, path):
        self.assets = {
            'some/file' : r'raw file bytes'.encode(),
            'some/other/file' : r'more file bytes'.encode()
        }
        self.metadata = {
            'some/file': { 'type': 'template' },
            'some/other/file': { 'type': 'static' }
        }
