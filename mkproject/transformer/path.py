from string import Template
from . import BaseTransformer
from . import TransformerError

class PathTransformer(BaseTransformer):
    name = 'path'
    @staticmethod
    def transform(cfg, path, data, meta):
        path_t = meta.get('path')
        if path_t is None:
            return path, data, meta
        context = {}
        context.update(meta)
        context.update(cfg)
        template = Template(path_t)
        try:
            path = template.substitute(**context)
        except (KeyError, TypeError) as e:
            raise TransformerError('path transformer failed on asset: {}: {}: {}'.format(path, e.__class__.__name__, e))
        return path, data, meta
