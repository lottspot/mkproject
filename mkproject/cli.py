import os
import sys
import argparse
import json
from pathlib import Path
from . import __pkg__
from . import Project
from . import LoaderError
from . import TransformerError
from . import DumperError
from .loader import MockLoader
from .dumper import MockDumper
from .loader.search import SearchLoader
from .loader.search import SearchLocation

CLI_HOME = Path.home() / '.{}'.format(__pkg__)

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
    rcpath = Path(CLI_HOME, 'config.json')
    try:
        with rcpath.open() as rcfile:
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

    # Base objects
    cfg = get_basecfg()
    parser = argparse.ArgumentParser()

    # CLI Interface
    parser.add_argument('-t', '--type', required=False, dest='projtype')
    parser.add_argument('name')
    parser.add_argument('config', nargs='*', default=[])

    # CLI values & config merge
    args = parser.parse_args()
    for pair in args.config:
        k, v = tokenize_kv(pair)
        cfg[k] = v
    cfg['name'] = args.name
    if args.projtype is not None:
        cfg['type'] = args.projtype

    # Validate finalized config
    if 'type' not in cfg.keys():
        die('missing required value -t/--type')

    # Config derived objects
    project = Project(cfg, SearchLoader, MockDumper)
    search_base = str(CLI_HOME / cfg['type'])
    load_location = SearchLocation(search_base)
    load_location.register_loader('', MockLoader)
    load_location.register_loader('.zip', MockLoader)
    dump_location = Path.cwd() / '{}-{}'.format(cfg['type'], cfg['name'])

    # Run
    try:
        project.make(load_location, dump_location)
    except LoaderError as e:
        die('error loading assets: {}'.format(e))
    except TransformerError as e:
        die('error transforming assets: {}'.format(e))
    except DumperError as e:
        die('error dumping project: {}'.format(e))

    # Tests
    print('cfg: {}'.format(cfg))

    return 0
