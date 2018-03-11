from string import Template
from . import BaseTransformer
from . import TransformerError

class TemplateTransformer(BaseTransformer):
    name = 'template'
    @staticmethod
    def transform(cfg, path, data, meta):
        context = {}
        context.update(meta)
        context.update(cfg)
        if hasattr(data, 'decode'):
            data = data.decode()
        template = Template(data)
        try:
            data = template.substitute(**context)
        except (KeyError, TypeError) as e:
            raise TransformerError('template transformer failed on asset {}: {}: {}'.format(path, e.__class__.__name__, e))
        return path, data, meta
