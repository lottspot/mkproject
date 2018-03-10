import unittest
from mkproject.dumper.fs import FSDumper
from pathlib import PurePosixPath

class MockFile():
    written = []
    @classmethod
    def clear(cls):
        cls.written = []
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        return self
    def __exit__(self, etype, eval, traceback):
        return
    def write(self, data):
        self.written.append((self.path, data))
        return len(data)

class MockPath(PurePosixPath):
    def mkdir(self, **kwargs):
        return
    def iterdir(self):
        return
        yield
    def open(self, mode=''):
        return MockFile(str(self))

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
        MockFile.clear()
        self.dumper = FSDumper('/dev/null')
        self.dumper._Path = MockPath
        self.pack = MockAssetPack()
    def test_dumper_fs_dumped_pack(self):
        assets = (
            ('a/1', 'data1'),
            ('2',   'data2'),
            ('a/3', 'data3')
        )
        files = (
            ('/dev/null/a/1', 'data1'),
            ('/dev/null/2',   'data2'),
            ('/dev/null/a/3', 'data3')
        )
        self.pack.assets = assets
        self.dumper.dump(self.pack)
        self.assertTupleEqual(files, tuple(MockFile.written))
