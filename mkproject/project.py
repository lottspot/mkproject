
class ProjectScaffold():
    def __init__(self):
        self._data = {}
    def register_path(self, path, data): pass
    def data(self, path): pass
    def paths(self): pass
    def project(self): pass

def render(cfg, asset_pack, render_class):
    project = ProjectScaffold()
    renderer = render_class(cfg, asset_pack)
    renderer.render(project)
    return project
