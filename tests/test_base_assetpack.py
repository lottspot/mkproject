import unittest
from mkproject.asset_pack import MockAssetPack
from mkproject.asset_pack.exceptions import NotLoadedError

class TestBaseAssetPack(unittest.TestCase):
    def setUp(self):
        self.pack = MockAssetPack('/dev/null')
    def test_assetpack_assets_notloaded(self):
        got_error = False
        try:
            self.pack._assets
        except NotLoadedError:
            got_error = True
        self.assertTrue(got_error)
    def test_assetpack_metadata_notloaded(self):
        got_error = False
        try:
            self.pack._metadata
        except NotLoadedError:
            got_error = True
        self.assertTrue(got_error)
    def test_assetpack_load(self):
        self.pack.load()
        self.pack._assets
        self.pack._metadata
