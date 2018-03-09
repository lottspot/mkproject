import unittest
from mkproject import LoaderError
from mkproject.loader.search import SearchLoader

class MockLoader():
    def __init__(self, location):
        self.location = location
    def load(self, pack):
        pack['loaded'] = self.location

class MockErrorLoader():
    def __init__(self, location): pass
    def load(self, pack): raise LoaderError()

class MockSearchLocation():
    def __init__(self):
        self.paths = None
    def get(self):
        return self.paths

class TestSearchLoader(unittest.TestCase):
    def setUp(self):
        self.location = MockSearchLocation()
        self.loader = SearchLoader(self.location)
        self.pack = {}
    def test_searchloader_load_first(self):
        self.location.paths = (
            ('/search/path/1', MockLoader),
            ('/search/path/2', MockLoader)
        )
        self.loader.load(self.pack)
        self.assertEqual(self.pack['loaded'], '/search/path/1')
    def test_searchloader_load_second(self):
        self.location.paths = (
            ('/search/path/1', MockErrorLoader),
            ('/search/path/2', MockLoader)
        )
        self.loader.load(self.pack)
        self.assertEqual(self.pack['loaded'], '/search/path/2')
