import unittest
from mkproject import LoaderError
from unittest.mock import MagicMock
from mkproject.loader.directory import DirectoryLoader

class TestDirectoryLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DirectoryLoader('/dev/null')
        self.loader._Path = MagicMock()
        self.pack = MagicMock()
        self.mfile = MagicMock()
        self.mdir = MagicMock()
        self.mdir.iterdir.side_effect = (
            (self.mfile, self.mfile, self.mdir), # data/     : data/a, data/b, data/sub
            (self.mfile, self.mfile),            # data/sub/ : data/sub/a, data/sub/b
        )
        self.mfile.relative_to.side_effect = (
            'a',
            'b',
            'sub/a',
            'sub/b',
        )
        self.mfile.read_bytes.side_effect = (
            b'data-a',                      # data/a
            b'{"meta-a":true}',             # meta/a.json
            b'data-b',                      # data/b
            FileNotFoundError,              # meta/b.json
            b'data-sub/a',                  # data/sub/a
            b'{"meta-sub/a":true}',         # meta/sub/a.json
            b'data-sub/b',                  # data/sub/b
            FileNotFoundError               # meta/sub/b.json
        )
        self.mdir.read_bytes.side_effect = IsADirectoryError
        self.mfile.iterdir.side_effect = NotADirectoryError
        self.loader._Path.side_effect = (
            self.mdir,
            self.mfile,
            self.mfile,
            self.mfile,
            self.mfile
        )
        self.assets = (
            ('a', b'data-a', {'meta-a': True}),
            ('b', b'data-b', {}),
            ('sub/a', b'data-sub/a', {'meta-sub/a': True}),
            ('sub/b', b'data-sub/b', {})
        )
    def test_loader_directory_loads(self):
        self.loader.load(self.pack)
        for asset in self.assets:
            self.pack.register_path.assert_any_call(*asset)
    def test_loader_directory_error(self):
        self.mfile.read_bytes.side_effect = ('', '', EnvironmentError)
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
    def test_loder_directory_jsonerror(self):
        self.mfile.read_bytes.side_effect = ('', '{]')
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
