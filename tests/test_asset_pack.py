import unittest
from mkproject.asset_pack import AssetPack

class TestAssetPack(unittest.TestCase):
    def setUp(self):
        self.mock_assets = (
                {'path': 'some/file', 'data': r'some file bytes'.encode(), 'meta': { 'type': 'template' }},
                {'path': 'some/other/file', 'data': r'other file bytes'.encode(), 'meta': { 'type': 'static' }}
        )
        self.pack = AssetPack()
        self.pack.register_path(self.mock_assets[0]['path'], self.mock_assets[0]['data'], **self.mock_assets[0]['meta'])
        self.pack.register_path(self.mock_assets[1]['path'], self.mock_assets[1]['data'], **self.mock_assets[1]['meta'])
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
    def test_assetpack_transform(self):
        pack = self.pack.transform()
        self.assertEqual(pack.data(self.mock_assets[0]['path']), self.mock_assets[0]['data'])
        self.assertEqual(pack.data(self.mock_assets[1]['path']), self.mock_assets[1]['data'])
    def test_assetpack_transform_pipeline(self):
        transformer_map = {
            'atob': lambda cfg, path, data, meta: (path, 'b', meta) if data == 'a' else (path, data, meta),
            'btoc': lambda cfg, path, data, meta: (path, 'c', meta) if data == 'b' else (path, data, meta)
        }
        self.pack.register_path('/data/a', 'a', pipeline=['atob', 'btoc'])
        pack = self.pack.transform(transformer_map, {})
        self.assertEqual(pack.data('/data/a'), 'c')
