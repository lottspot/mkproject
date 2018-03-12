import unittest
from mkproject import LoaderError
from unittest.mock import MagicMock
from mkproject.loader.directory import DirectoryLoader

class TestDirectoryLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DirectoryLoader('/dev/null')
        self.loader._Path = MagicMock()
        self.pack = MagicMock()
        self.assets = (
            ('a', b'data-a', {'meta-a': True}),
            ('b', b'data-b', {}),
            ('sub/a', b'data-sub/a', {'meta-sub/a': True}),
            ('sub/b', b'data-sub/b', {})
        )
        self.directory = {
            'data/': MagicMock(**{
                'read_bytes.side_effect': IsADirectoryError
            }),
            'data/a': MagicMock(**{
                'read_bytes.return_value': b'data-a',
                'relative_to.return_value': 'a',
                'iterdir.side_effect': NotADirectoryError,
            }),
            'data/b': MagicMock(**{
                'read_bytes.return_value': b'data-b',
                'relative_to.return_value': 'b',
                'iterdir.side_effect': NotADirectoryError,
            }),
            'data/sub/': MagicMock(**{
                'read_bytes.side_effect': IsADirectoryError
            }),
            'data/sub/a': MagicMock(**{
                'read_bytes.return_value': b'data-sub/a',
                'relative_to.return_value': 'sub/a',
                'iterdir.side_effect': NotADirectoryError,
            }),
            'data/sub/b': MagicMock(**{
                'read_bytes.return_value': b'data-sub/b',
                'relative_to.return_value': 'sub/b',
                'iterdir.side_effect': NotADirectoryError,
            }),
        }
        self.directory['data/'].iterdir.return_value = (
            self.directory['data/a'],
            self.directory['data/b'],
            self.directory['data/sub/'],
        )
        self.directory['data/sub/'].iterdir.return_value = (
            self.directory['data/sub/a'],
            self.directory['data/sub/b'],
        )
        self.meta_files = {
            'meta/a.json': MagicMock(**{
                'read_bytes.return_value': b'{"meta-a":true}',
            }),
            'meta/sub/a.json': MagicMock(**{
                'read_bytes.return_value': b'{"meta-sub/a":true}',
            }),
        }
        nofile = MagicMock(**{'read_bytes.side_effect':FileNotFoundError})
        self.loader._Path.side_effect = lambda *args: self.directory['data/'] if args[1] == 'data' else self.meta_files.get('/'.join(args[1:]), nofile)
    def test_loader_directory_loads(self):
        self.loader.load(self.pack)
        for asset in self.assets:
            self.pack.register_path.assert_any_call(*asset)
    def test_loader_directory_error(self):
        self.directory['data/a'].read_bytes.side_effect = EnvironmentError
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
    def test_loder_directory_jsonerror(self):
        self.meta_files['meta/sub/a.json'].read_bytes.return_value = '{]'
        try:
            self.loader.load(self.pack)
        except LoaderError:
            return
        raise AssertionError('Unexpected test pass')
