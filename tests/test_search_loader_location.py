import unittest
from mkproject.loader.search import SearchLocation

class TestSearchLocation(unittest.TestCase):
    def setUp(self):
        self.base = '/dev/null'
        self.location = SearchLocation(self.base)
    def test_searchlocation_base(self):
        self.assertTrue(self.base == self.location.base)
    def test_searchlocation_get(self):
        loader1 = ('/tail1', 'loader1')
        loader2 = ('/tail2', 'loader2')
        self.location.register_loader(*loader1)
        self.location.register_loader(*loader2)
        expect = ((self.base + '/tail1', 'loader1'), (self.base + '/tail2', 'loader2'))
        loaders = self.location.get()
        self.assertTupleEqual(expect, loaders)
