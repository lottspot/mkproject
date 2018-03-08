import unittest
from mkproject import assets
from mkproject.asset_loader import MockAssetLoader

class TestBaseAssetPack(unittest.TestCase):
    def setUp(self):
        self.mock_assets = (
                {'path': 'some/file', 'data': r'some file bytes'.encode(), 'meta': { 'type': 'template' }},
                {'path': 'some/other/file', 'data': r'other file bytes'.encode(), 'meta': { 'type': 'static' }}
        )
        self.pack = assets.load(self.mock_assets, MockAssetLoader)
    def test_assetpack_data(self):
        asset = self.mock_assets[0]
        data = self.pack.data(asset['path'])
        self.assertEqual(data, asset['data'])
    def test_assetpack_meta(self):
        asset = self.mock_assets[0]
        meta = self.pack.meta(asset['path'])
        self.assertDictEqual(meta, asset['meta'])
    def test_assetpack_paths(self):
        expect = (self.mock_assets[0]['path'], self.mock_assets[1]['path'])
        paths = self.pack.paths()
        self.assertTupleEqual(expect, paths)
    def test_assetpack_assets(self):
        expect = tuple(self.mock_assets)
        assets = self.pack.assets()
        self.assertTupleEqual(expect, assets)
