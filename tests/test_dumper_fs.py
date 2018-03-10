import unittest
from pathlib import PurePosixPath
from mkproject import DumperError
from unittest.mock import MagicMock
from mkproject.dumper.fs import FSDumper

class TestFSDumper(unittest.TestCase):
    def setUp(self):
        self.dumper = FSDumper('/dev/null')
        self.dumper._Path = MagicMock()
        self.pack = MagicMock()
    def test_dumper_fs_dumped_pack(self):
        path = MagicMock()
        self.pack.paths.return_value = ('a','b','c')
        self.pack.data.side_effect = ('data-a', 'data-b', 'data-c')
        self.dumper._Path.return_value = path
        self.dumper.dump(self.pack)
        self.dumper._Path.called_any(path, 'a')
        self.dumper._Path.called_any(path, 'b')
        self.dumper._Path.called_any(path, 'c')
        path.write_bytes.called_any('data-a')
        path.write_bytes.called_any('data-b')
        path.write_bytes.called_any('data-c')
    def test_dumper_fs_dumped_pack_withparents(self):
        path = MagicMock()
        path.write_bytes.side_effect = [FileNotFoundError, path]
        self.pack.paths.return_value = ('a',)
        self.pack.data.side_effect = ('data',)
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
        base.iterdir.return_value = ['a', 'b']
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
        self.pack.paths.return_value = ('a',)
        self.pack.data.side_effect = ('data',)
        self.dumper._Path.return_value = path
        try:
            self.dumper.dump(self.pack)
        except DumperError:
            path.write_bytes.assert_called_once()
            return
        raise RuntimeError('Unexpected test pass')
    def test_dumper_fs_data_encode(self):
        data = MagicMock()
        self.pack.paths.return_value = ('a',)
        self.pack.data.side_effect = (data,)
        self.dumper.dump(self.pack)
        data.encode.assert_called_once()
