
class BaseAssetSearch():
    def __init__(self, cfg):
        self._cfg = cfg
    def search(self, term):
        raise NotImplementedError()

class MockAssetSearch(BaseAssetSearch):
    def search(self, term):
        return term
