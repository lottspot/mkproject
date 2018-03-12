import unittest
from zipfile import BadZipFile
from zipfile import LargeZipFile
from mkproject import LoaderError
from unittest.mock import MagicMock
from mkproject.loader.zipfile import ZipfileLoader

class TestZipfileLoader(unittest.TestCase):
    def setUp(self):
        self.pack = MagicMock()
        self.loader = ZipfileLoader('/dev/null')
        self.loader._ZipFile = MagicMock()
        self.infolist = (
            MagicMock(**{'filename':'data/', 'is_dir.return_value':True}),
            MagicMock(**{'filename':'data/a', 'is_dir.return_value':False}),
            MagicMock(**{'filename':'data/b', 'is_dir.return_value':False}),
            MagicMock(**{'filename':'data/sub/', 'is_dir.return_value':True}),
            MagicMock(**{'filename':'data/sub/a', 'is_dir.return_value':False}),
            MagicMock(**{'filename':'data/sub/b', 'is_dir.return_value':False}),
            MagicMock(**{'filename':'meta/', 'is_dir.return_value':True}),
            MagicMock(**{'filename':'meta/a.json', 'is_dir.return_value':False}),
            MagicMock(**{'filename':'meta/sub/a.json', 'is_dir.return_value':False})
        )
        self.archive = {
            'data/': b'',
            'data/a': b'data-a',
            'data/b': b'data-b',
            'data/sub/': b'',
            'data/sub/a': b'data-sub/a',
            'data/sub/b': b'data-sub/b',
            'meta/': b'',
            'meta/a.json': b'{"meta-a":true}',
            'meta/sub/': b'',
            'meta/sub/a.json': b'{"meta-sub/a":true}'
        }
        self.loader._ZipFile().__enter__().infolist.return_value = self.infolist
        self.loader._ZipFile().__enter__().read.side_effect = lambda path: self.archive[path]
    def test_loader_zipfile_loads(self):
        assets = (
            ('a', b'data-a', {'meta-a': True}),
            ('b', b'data-b', {}),
            ('sub/a', b'data-sub/a', {'meta-sub/a': True}),
            ('sub/b', b'data-sub/b', {})
        )
        self.loader.load(self.pack)
        for asset in assets:
            self.pack.register_path.assert_any_call(*asset)
    def test_loader_zipfile_enverror(self):
        self.loader._ZipFile().__enter__().read.side_effect = EnvironmentError
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
    def test_loader_zipfile_badziperror(self):
        self.loader._ZipFile().__enter__.side_effect = BadZipFile
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
    def test_loader_zipfile_largeziperror(self):
        self.loader._ZipFile().__enter__.side_effect = LargeZipFile
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
    def test_loder_zipfile_jsonerror(self):
        self.archive['meta/a.json'] = b'{]'
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
