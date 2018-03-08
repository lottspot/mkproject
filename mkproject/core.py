from . import assets
from . import project

class Core():
    def __init__(self, asset_loader, asset_search, project_dumper, project_renderer):
        self._loader = asset_loader
        self._search = asset_search
        self._dumper = project_dumper
        self._renderer = project_renderer
    def load_assets(self, location): pass
    def find_and_load_assets(self, search_term): pass
    def render_project(self, cfg): pass
    def dump_project(self, location): pass
    def run(self, render_cfg, load_location, dump_location): pass
    def find_and_run(self, render_cfg, search_term, dump_location): pass
