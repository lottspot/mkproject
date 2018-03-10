import os
from pathlib import Path
from . import BaseDumper
from . import DumperError

class FSDumper(BaseDumper):
    Path = Path
    def dump(self, pack):
        base = self.Path(self._location)
        dirlist = []
        try:
            dirlist = [ f for f in base.iterdir() ]
        except FileNotFoundError:
            try:
                base.mkdir()
            except EnvironmentError as e:
                raise DumperError(e.strerror)
        except EnvironmentError as e:
            raise DumperError(e.strerror)
        if len(dirlist) > 0:
            raise DumperError('non-empty directory: {}'.format(str(base)))
        for pathtail in pack.paths():
            path = self.Path(base, pathtail)
            data = pack.data(pathtail)
            try:
                self._write_path(path, data)
            except FileNotFoundError:
                try:
                    path.parent.mkdir(parents=True)
                    self._write_path(path, data)
                except EnvironmentError as e:
                    raise DumperError(e.strerror)
            except EnvironmentError as e:
                raise DumperError(e.strerror)
    def _write_path(self, path, data):
        with path.open('w') as fd:
            fd.write(data)
