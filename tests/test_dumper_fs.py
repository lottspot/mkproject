import unittest
from pathlib import PurePosixPath
from mkproject import DumperError
from unittest.mock import MagicMock
from mkproject.dumper.fs import FSDumper

class MockAssetPack():
    def __init__(self, assets=()):
        self.assets = assets
    def paths(self):
        paths = []
        for path, data in self.assets:
            paths.append(path)
        return paths
    def data(self, dpath):
        for path, data in self.assets:
            if dpath == path:
                return data

class TestFSDumper(unittest.TestCase):
    def setUp(self):
        self.dumper = FSDumper('/dev/null')
        self.dumper._Path = MagicMock()
        self.pack = MockAssetPack()
    def test_dumper_fs_dumped_pack(self):
        assets = (
            ('a/1', 'data1'),
            ('2',   'data2'),
            ('a/3', 'data3')
        )
        path = MagicMock()
        self.pack.assets = assets
        self.dumper._Path.return_value = path
        self.dumper.dump(self.pack)
        self.dumper._Path.called_any(path, 'a/1')
        self.dumper._Path.called_any(path, '2')
        self.dumper._Path.called_any(path, 'a/3')
        path.write_bytes.called_any('data1')
        path.write_bytes.called_any('data2')
        path.write_bytes.called_any('data3')
    def test_dumper_fs_dumped_pack_withparents(self):
        path = MagicMock()
        path.write_bytes.side_effect = [FileNotFoundError, path]
        self.pack.assets = [('a/1', 'data')]
        self.dumper._Path.return_value = path
        self.dumper.dump(self.pack)
        path.parent.mkdir.assert_called_once_with(parents=True)
    def test_dumper_fs_location_create(self):
        base = MagicMock()
        base.iterdir.side_effect = FileNotFoundError
        self.dumper._Path.side_effect = [base]
        self.dumper.dump(self.pack)
        base.iterdir.assert_called_once()
        base.mkdir.assert_called_once()
    def test_dumper_fs_location_nonempty(self):
        base = MagicMock()
        base.iterdir.return_value = ['1', '2']
        self.dumper._Path.side_effect = [base]
        try:
            self.dumper.dump(self.pack)
        except DumperError as e:
            base.iterdir.assert_called_once()
            self.assertTrue(str(e).startswith('non-empty directory'))
            return
        raise RuntimeError('Unexpected test pass')
    def test_dumper_fs_dump_enverror(self):
        path = MagicMock()
        path.write_bytes.side_effect = EnvironmentError
        self.pack.assets = [('a/1', 'data')]
        self.dumper._Path.return_value = path
        try:
            self.dumper.dump(self.pack)
        except DumperError:
            path.write_bytes.assert_called_once()
            return
        raise RuntimeError('Unexpected test pass')
    def test_dumper_fs_data_encode(self):
        data = MagicMock()
        self.pack.assets = [('a/1', data)]
        self.dumper.dump(self.pack)
        data.encode.assert_called_once()
