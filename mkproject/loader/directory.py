import json
from pathlib import Path
from . import BaseLoader
from . import LoaderError

class DirectoryLoader(BaseLoader):
    _Path = Path
    def load(self, pack):
        base = self._Path(self.location, 'data')
        try:
            self._traverse(base, pack, base)
        except EnvironmentError as e:
            raise LoaderError('failed to load asset pack {}: {}'.format(self.location, e))
    def _traverse(self, path, pack, top_level):
        for item in path.iterdir():
            try:
                self._traverse(item, pack, top_level)
            except NotADirectoryError:
                asset_path = item.relative_to(top_level)
                asset_data = item.read_bytes()
                asset_meta = {}
                meta_path = self._meta_path(asset_path)
                try:
                    asset_meta = json.loads(meta_path.read_bytes())
                except FileNotFoundError:
                    pass
                except json.decoder.JSONDecodeError as e:
                    raise LoaderError('failed to load meta {}: {}: {}'.format(meta_path, e.__class__.__name__, e))
                pack.register_path(asset_path, asset_data, asset_meta)
                self.log('- {}'.format(path))
    def _meta_path(self, asset_path):
        name = str(asset_path) + '.json'
        path = self._Path(self.location, 'meta', name)
        return path
