import os
import sys
import argparse
import json
from pathlib import Path
from .asset_pack import MockAssetPack

__version__ = '0.0.0'
__pkg__     = 'mkproject'

CLI_HOME   = Path.home() / '.{}'.format(__pkg__)
CLI_RCFILE = Path(CLI_HOME, 'config.json')

def get_basecfg():
    basecfg = {}
    if CLI_RCFILE.exists():
        with CLI_RCFILE.open() as rcfile:
            data = rcfile.read()
            basecfg = json.loads(data.decode())
    return basecfg

def find_asset_pack(projtype):
    search_base = str(Path(CLI_HOME, projtype))
    try_exstensions = (
        ('', MockAssetPack),
        ('.zip', MockAssetPack),
    )
    for ext, packobj in try_exstensions:
        with_ext = search_base + ext
        try_path = Path(with_ext)
        if try_path.exists():
            return packobj(try_path)
    return None

def die(msg):
    emsg = '{}: fatal: {}'.format(
        os.path.basename(sys.argv[0]),
        msg
    )
    sys.exit(emsg)

def main():
    cfg = get_basecfg()
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--type', required=False, dest='projtype')
    parser.add_argument('name')
    parser.add_argument('config', nargs='*', default=[])

    args = parser.parse_args()

    cfg['name'] = args.name
    if args.projtype is not None:
        cfg['type'] = args.projtype
    if 'type' not in cfg.keys():
        die('no project type provided; add type to config file or specify using -t')
    cfg['asset_pack'] = find_asset_pack(cfg['type'])
    for pair in args.config:
        i = pair.find(':')
        k = None
        v = ''
        if i < 0:
            k = pair
        elif len(pair) - 1 == i:
            k = pair[:i]
        else:
            k = pair[:i]
            v = pair[i+1:]
        cfg[k] = v

    print('cfg: {}'.format(cfg))

    return 0
