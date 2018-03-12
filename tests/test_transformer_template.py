import unittest
from mkproject import TransformerError
from unittest.mock import MagicMock
from mkproject.transformer.template import TemplateTransformer

class TestTemplateTransformer(unittest.TestCase):
    def setUp(self):
        self.asset = ['/dev/null', '$foo', {'foo': 'baz'}]
        self.cfg = { 'foo': 'bar' }
    def test_transformer_template_renders_str(self):
        path, data, meta = TemplateTransformer.transform(self.cfg, *self.asset)
        self.assertEqual(data, 'bar')
    def test_transformer_template_renders_bytes(self):
        self.asset[1] = rb'$foo'
        path, data, meta = TemplateTransformer.transform(self.cfg, *self.asset)
        self.assertEqual(data, 'bar')
    def test_transformer_template_error(self):
        self.asset[1] = '$bar'
        try:
            path, data, meta = TemplateTransformer.transform(self.cfg, *self.asset)
        except TransformerError:
            return
        raise AssertionError('Unexpected test pass')
