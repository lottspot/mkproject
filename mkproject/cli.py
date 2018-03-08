import os
import sys
import argparse
import json
from pathlib import Path
from . import __pkg__
from . import assets
from .core import Core
from .asset_loader import MockAssetLoader
from .project_renderer import MockProjectRenderer
from .project_dumper import MockProjectDumper
from .asset_loader.search import SearchAssetLoader
from .asset_loader.search import SearchLocation

CLI_HOME   = Path.home() / '.{}'.format(__pkg__)
CLI_RCFILE = Path(CLI_HOME, 'config.json')

def tokenize_kv(kvstr):
    delim = ':'
    k = ''
    v = ''
    i = kvstr.find(delim)
    if i < 0:
        k = kvstr
    else:
        k = kvstr[:i]
        try:
            v = kvstr[i+1:]
        except IndexError:
            pass
    return k, v

def get_basecfg():
    basecfg = {}
    try:
        with CLI_RCFILE.open() as rcfile:
            data = rcfile.read()
            basecfg = json.loads(data.decode())
    except OSError as e:
        pass
    return basecfg

def die(msg):
    emsg = '{}: fatal: {}'.format(
        os.path.basename(sys.argv[0]),
        msg
    )
    sys.exit(emsg)

def main():
    core = Core(SearchAssetLoader, MockProjectDumper, MockProjectRenderer)
    cfg = get_basecfg()
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--type', required=True, dest='projtype')
    parser.add_argument('name')
    parser.add_argument('config', nargs='*', default=[])

    args = parser.parse_args()

    for pair in args.config:
        k, v = tokenize_kv(pair)
        cfg[k] = v
    cfg['name'] = args.name
    cfg['type'] = args.projtype

    pack_location = SearchLocation(str(CLI_HOME / cfg['type']))
    pack_location.register_loader('', MockAssetLoader)
    pack_location.register_loader('.zip', MockAssetLoader)

    dump_location = Path.cwd() / '{}-{}'.format(cfg['type'], cfg['name'])

    try:
        core.run(cfg, pack_location, dump_location)
    except assets.LoaderError:
        die('no asset packs for project type: {}'.format(cfg['type']))

    # Tests
    print('cfg: {}'.format(cfg))

    return 0
