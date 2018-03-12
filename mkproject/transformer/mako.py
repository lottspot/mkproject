from . import BaseTransformer
from . import TransformerError
from mako.template import Template

class MakoTransformer(BaseTransformer):
    name = 'mako'
    @staticmethod
    def transform(cfg, path, data, meta):
        context = {}
        context.update(cfg)
        context['asset_path'] = path
        context['asset_meta'] = meta
        try:
            template = Template(data)
            data = template.render(**context)
        except Exception as e:
            raise TransformerError('mako transformer failed on asset {}: {}: {}'.format(path, e.__class__.__name__, e))
        return path, data, meta
