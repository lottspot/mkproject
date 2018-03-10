import os
from pathlib import Path
from . import BaseDumper
from . import DumperError

class FSDumper(BaseDumper):
    _Path = Path
    def dump(self, pack):
        base = self._Path(self._location)
        dirlist = []
        try:
            try:
                dirlist = [ f for f in base.iterdir() ]
            except FileNotFoundError:
                base.mkdir()
            if len(dirlist) > 0:
                raise DumperError('non-empty directory: {}'.format(str(base)))
            for pathtail in pack.paths():
                path = self._Path(base, pathtail)
                data = pack.data(pathtail)
                if hasattr(data, 'encode'):
                    data = data.encode()
                try:
                    path.write_bytes(data)
                except FileNotFoundError:
                    path.parent.mkdir(parents=True)
                    path.write_bytes(data)
        except EnvironmentError as e:
            raise DumperError(e.strerror)
