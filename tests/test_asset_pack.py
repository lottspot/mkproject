import unittest
from mkproject.asset_pack import AssetPack
from mkproject.asset_loader import MockAssetLoader
from mkproject.exceptions import AssetLoaderError

class TestBaseAssetPack(unittest.TestCase):
    def setUp(self):
        self.mock_assets = (
                {'pathname': 'some/file', 'data': r'some file bytes'.encode(), 'meta': { 'type': 'template' }},
                {'pathname': 'some/other/file', 'data': r'other file bytes'.encode(), 'meta': { 'type': 'static' }}
        )
        self.pack = AssetPack()
        self.pack.loader = MockAssetLoader(self.mock_assets)
    def test_assetpack_notloaded(self):

        got_error = False
        try:
            self.pack.data('some/file')
        except AssetLoaderError:
            got_error = True
        self.assertTrue(got_error, 'data')

        got_error = False
        try:
            self.pack.meta('some/file')
        except AssetLoaderError:
            got_error = True
        self.assertTrue(got_error, 'meta')

        got_error = False
        try:
            self.pack.pathnames('some/file')
        except AssetLoaderError:
            got_error = True
        self.assertTrue(got_error, 'pathnames')

        got_error = False
        try:
            self.pack.paths('some/file')
        except AssetLoaderError:
            got_error = True
        self.assertTrue(got_error, 'paths')

    def test_assetpack_data(self):
        self.pack.load()
        asset = self.mock_assets[0]
        data = self.pack.data(asset['pathname'])
        self.assertEqual(data, asset['data'])
    def test_assetpack_meta(self):
        self.pack.load()
        asset = self.mock_assets[0]
        meta = self.pack.meta(asset['pathname'])
        self.assertDictEqual(meta, asset['meta'])
    def test_assetpack_pathnames(self):
        self.pack.load()
        expect = (self.mock_assets[0]['pathname'], self.mock_assets[1]['pathname'])
        pathnames = self.pack.pathnames()
        self.assertTupleEqual(expect, pathnames)
    def test_assetpack_paths(self):
        self.pack.load()
        expect = tuple(self.mock_assets)
        paths = self.pack.paths()
        self.assertTupleEqual(expect, paths)
