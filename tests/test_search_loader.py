import unittest
from mkproject import LoaderError
from unittest.mock import MagicMock
from mkproject.loader.search import SearchLoader

class TestSearchLoader(unittest.TestCase):
    def setUp(self):
        self.location = MagicMock()
        self.loader = SearchLoader(self.location)
    def test_searchloader_load_first(self):
        loader = MagicMock()
        self.location.get.return_value = (
            ('/search/path/1', loader),
            ('/search/path/2', loader)
        )
        self.loader.load(None)
        loader().load.assert_called_once_with(None)
    def test_searchloader_load_second(self):
        loader = MagicMock()
        eloader = MagicMock()
        eloader().load.side_effect = LoaderError
        self.location.get.return_value = (
            ('/search/path/1', eloader),
            ('/search/path/2', loader)
        )
        self.loader.load(None)
        loader().load.assert_called_once_with(None)
