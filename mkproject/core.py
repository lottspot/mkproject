from . import assets
from . import project

class Core():
    def __init__(self, asset_loader, project_dumper, project_renderer):
        self._loader = asset_loader
        self._dumper = project_dumper
        self._renderer = project_renderer
    def load_assets(self, location):
        self._pack = assets.load(location, self._loader)
    def render_project(self, cfg):
        try:
            pack = self._pack
        except AttributeError:
            raise RuntimeError('must call load_assets before render_project')
        self._project = project.render(cfg, pack, self._renderer)
    def dump_project(self, location):
        try:
            proj = self._project
        except AttributeError:
            raise RuntimeError('must call render_project before dump_project')
        project.dump(location, proj, self._dumper)
    def run(self, render_cfg, load_location, dump_location):
        self.load_assets(load_location)
        self.render_project(render_cfg)
        self.dump_project(dump_location)
