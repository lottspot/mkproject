import unittest
from mkproject import TransformerError
from mkproject.transformer.path import PathTransformer

class TestPathTransformer(unittest.TestCase):
    def setUp(self):
        self.asset = [ '/dev/null', rb'\x00', {'foo': 'bar', 'path': '/dev/null/$foo'} ]
        self.cfg = {'foo': 'baz'}
    def test_transformer_path_renders(self):
        path, data, meta = PathTransformer.transform(self.cfg, *self.asset)
        self.assertEqual(path, '/dev/null/baz')
    def test_transformer_template_error(self):
        self.asset[2]['path'] = '/dev/null/$bar'
        try:
            path, data, meta = PathTransformer.transform(self.cfg, *self.asset)
        except TransformerError:
            return
        raise AssertionError('Unexpected test pass')
