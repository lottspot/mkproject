import unittest
from mkproject.assets import AssetPack
from mkproject.project import ProjectScaffold

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
        proj = self.pack.transform()
        self.assertEqual(proj.data(self.mock_assets[0]['path']), self.mock_assets[0]['data'])
        self.assertEqual(proj.data(self.mock_assets[1]['path']), self.mock_assets[1]['data'])
