from .project_dumper import ProjectDumperError as DumperError

ProjectDumperError = DumperError

class ProjectScaffold():
    def __init__(self):
        self._data = {}
    def register_path(self, path, data):
        self._data[path] = data
    def data(self, path):
        try:
            return self._data[path]
        except KeyError:
            raise AttributeError('No data for path: {}'.format(path))
    def paths(self):
        return tuple(self._data.keys())
    def project(self):
        project = []
        for path in self._data.keys():
            project.append({
                'path': path,
                'data': self.data(path)
            })
        return tuple(project)

def dump(location, project, dump_class):
    dumper = dump_class(location)
    dumper.dump(project)
