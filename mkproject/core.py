from . import assets
from . import project

class Core():
    def __init__(self, asset_loader, project_dumper, project_renderer):
        self._loader = asset_loader
        self._dumper = project_dumper
        self._renderer = project_renderer
    def load_assets(self, location): pass
    def render_project(self, cfg): pass
    def dump_project(self, location): pass
    def run(self, render_cfg, load_location, dump_location): pass
