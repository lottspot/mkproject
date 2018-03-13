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
from .dumper.fs import FSDumper
from .loader.directory import DirectoryLoader
from .loader.zipfile import ZipfileLoader
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
        data = rcpath.read_bytes()
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
    DirectoryLoader.log = print
    ZipfileLoader.log = print
    FSDumper.log = print

    # CLI Interface
    parser.add_argument('-d', '--directory', required=False, dest='dump_location')
    parser.add_argument('-t', '--type', required=False, dest='projtype')
    parser.add_argument('name')
    parser.add_argument('config', nargs='*', default=[])

    # CLI values & config merge
    args = parser.parse_args()
    for pair in args.config:
        k, v = tokenize_kv(pair)
        cfg[k] = v
    cfg['project_name'] = args.name
    if args.projtype is not None:
        cfg['project_type'] = args.projtype

    # Validate finalized config
    if 'type' not in cfg.keys():
        die('missing required value -t/--type')

    # Config derived objects
    project = Project(cfg, SearchLoader, FSDumper)
    search_base = Path(CLI_HOME, 'assets', cfg['project_type'])
    load_location = SearchLocation(str(search_base))
    load_location.register_loader('', DirectoryLoader)
    load_location.register_loader('.zip', ZipfileLoader)
    dump_location = Path('{}-{}'.format(cfg['project_type'], cfg['project_name']))
    if args.dump_location is not None:
        dump_location = args.dump_location

    # Run
    try:
        project.make(load_location, dump_location)
    except LoaderError as e:
        die('load error: {}'.format(e))
    except TransformerError as e:
        die('transform error: {}'.format(e))
    except DumperError as e:
        die('dump error: {}'.format(e))

    return 0
