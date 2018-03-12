import unittest
from mkproject import TransformerError
from mkproject.transformer.mako import MakoTransformer

class TestMakoTransformer(unittest.TestCase):
    def setUp(self):
        self.asset = [ '/dev/null', r'${foo}', {} ]
        self.cfg = {'foo': 'bar'}
    def test_transformer_mako_renders(self):
        path, data, meta = MakoTransformer.transform(self.cfg, *self.asset)
        self.assertEqual(data, 'bar')
    def test_transformer_mako_error(self):
        self.asset[1] = r'${bar}'
        try:
            path, data, meta = MakoTransformer.transform(self.cfg, *self.asset)
        except TransformerError:
            return
        raise AssertionError('Unexpected test pass')
