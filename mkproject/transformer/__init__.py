from collections.abc import MutableMapping

def transform(cfg, path, data, meta):
    return path, data, meta

class BaseTransformer():
    @staticmethod
    @property
    def name():
        raise NotImplementedError()
    @staticmethod
    def transform(cfg, path, data, meta):
        return path, data, meta

class TransformerMap(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._map = dict(*args, **kwargs)
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self._map))
    def __str__(self):
        return str(self._map)
    # Begin MutableMapping methods
    def __len__(self):
        return self._map.__len__()
    def __getitem__(self, key):
        return self._map.__getitem__(key)
    def __setitem__(self, key, value):
        return self._map.__setitem__(key, value)
    def __delitem__(self, key):
        return self._map.__delitem__(key)
    def __iter__(self):
        return self._map.__iter__()
    # Begin dict methods
    def copy(self):
        copy = self.__class__()
        copy._map = self._map.copy()
        return copy
    # Begin TransformerMap methods
    def add(self, transformer):
        self[transformer.name] = transformer

class TransformerError(Exception): pass
