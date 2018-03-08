import unittest
from mkproject import assets
from mkproject.asset_loader import MockAssetLoader

class TestBaseAssetPack(unittest.TestCase):
    def setUp(self):
        self.mock_assets = (
                {'pathname': 'some/file', 'data': r'some file bytes'.encode(), 'meta': { 'type': 'template' }},
                {'pathname': 'some/other/file', 'data': r'other file bytes'.encode(), 'meta': { 'type': 'static' }}
        )
        self.pack = assets.load(self.mock_assets, MockAssetLoader)
    def test_assetpack_data(self):
        asset = self.mock_assets[0]
        data = self.pack.data(asset['pathname'])
        self.assertEqual(data, asset['data'])
    def test_assetpack_meta(self):
        asset = self.mock_assets[0]
        meta = self.pack.meta(asset['pathname'])
        self.assertDictEqual(meta, asset['meta'])
    def test_assetpack_paths(self):
        expect = (self.mock_assets[0]['pathname'], self.mock_assets[1]['pathname'])
        paths = self.pack.paths()
        self.assertTupleEqual(expect, paths)
    def test_assetpack_assets(self):
        expect = tuple(self.mock_assets)
        assets = self.pack.assets()
        self.assertTupleEqual(expect, assets)
