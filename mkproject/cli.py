import os
import sys
import argparse
import json
from pathlib import Path
from . import __pkg__
from . import assets
from .asset_loader import MockAssetLoader

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

def load_project_pack(projtype):
    search_base = str(Path(CLI_HOME, projtype))
    try_exstensions = (
        ('', MockAssetLoader),
        ('.zip', MockAssetLoader),
    )
    for ext, loader_class in try_exstensions:
        with_ext = search_base + ext
        try_path = Path(with_ext)
        try:
            return assets.load(try_path, loader_class)
        except assets.LoaderError:
            continue
    raise RuntimeError('Failed to load asset pack for project {} from {}'.format(project, search_base))

def die(msg):
    emsg = '{}: fatal: {}'.format(
        os.path.basename(sys.argv[0]),
        msg
    )
    sys.exit(emsg)

def main():
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

    try:
        cfg['asset_pack'] = load_project_pack(cfg['type'])
    except RuntimeError:
        die('no asset packs for project type: {}'.format(cfg['type']))

    # Tests
    cfg['asset_pack'].assets
    cfg['asset_pack'].metadata
    print('cfg: {}'.format(cfg))

    return 0