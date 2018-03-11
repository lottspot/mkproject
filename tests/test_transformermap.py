import unittest
from mkproject import TransformerMap
from unittest.mock import MagicMock

class TestTransformerMap(unittest.TestCase):
    def setUp(self):
        self.map = TransformerMap()
        self.t = MagicMock()
        self.t.name = 'transformer'
    def test_transformermap_add(self):
        self.map.add(self.t)
        self.assertEqual(self.map['transformer'], self.t)
    def test_transformermap_copy(self):
        self.map['a'] = 1
        copy = self.map.copy()
        self.assertEqual(self.map, copy, 'unequal after initial copy')
        self.assertTrue(hasattr(copy, 'add'), 'copy is not a TransformerMap')
        self.map['b'] = 2
        self.assertTrue('b' not in copy.keys(), 'dict is shared not copied')
