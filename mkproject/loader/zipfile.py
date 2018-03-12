import json
import zipfile
from . import BaseLoader
from . import LoaderError

class ZipfileLoader(BaseLoader):
    _ZipFile = zipfile.ZipFile
    def load(self, pack):
        data_prefix = 'data/'
        meta_prefix = 'meta/'
        try:
            with self._ZipFile(self.location) as z:
                for item in z.infolist():
                    if item.filename.startswith(data_prefix) and not item.is_dir():
                        path = item.filename[len(data_prefix):]
                        data = z.read(item.filename)
                        meta = {}
                        meta_key = meta_prefix + path + '.json'
                        try:
                            meta = json.loads(z.read(meta_key))
                        except KeyError:
                            pass
                        except json.decoder.JSONDecodeError as e:
                            raise LoaderError('Failed to load meta: {}: {}: {}'.format(self.location, e.__class__.__name__, e))
                        pack.register_path(path, data, meta)
        except (EnvironmentError, zipfile.BadZipFile, zipfile.LargeZipFile) as e:
            raise LoaderError('failed to load asset pack {}: {}: {}'.format(self.location, e.__class__.__name__, e))
