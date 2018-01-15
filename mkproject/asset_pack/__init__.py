
class BaseAssetPack():
    assets = None
    metadata = None
    def __init__(self, path):
        self._load_assets(path)
    def _load_assets(self, path):
        # Method must be implemented by concrete asset pack types
        raise NotImplementedError()

class MockAssetPack():
    def _load_assets(self, path):
        self.assets = {
            'some/file' : r'raw file bytes'.encode(),
            'some/other/file' : r'more file bytes'.encode()
        }
        self.metadata = {
            'some/file': { 'type': 'template' },
            'some/other/file': { 'type': 'static' }
        }
