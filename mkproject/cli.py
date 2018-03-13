import os
import sys
import argparse
import json
from pathlib import Path
from . import __pkg__
from . import __version__
from . import Project
from . import LoaderError
from . import TransformerError
from . import DumperError
from . import TransformerMap
from .dumper.fs import FSDumper
from .loader.directory import DirectoryLoader
from .loader.zipfile import ZipfileLoader
from .loader.search import SearchLoader
from .loader.search import SearchLocation
from .transformer.template import TemplateTransformer
from .transformer.path import PathTransformer
from .transformer.mako import MakoTransformer


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
    tmap = TransformerMap()
    tmap.add(TemplateTransformer)
    tmap.add(PathTransformer)
    tmap.add(MakoTransformer)
    DirectoryLoader.log = print
    ZipfileLoader.log = print
    FSDumper.log = print

    # CLI Interface
    parser.add_argument('-d', '--directory', required=False, dest='dump_location', help='directory to output project files into')
    parser.add_argument('-t', '--type', required=False, dest='project_type', help='name of the project type to source templates from')
    parser.add_argument('project_name', help='name of the new project')
    parser.add_argument('config', nargs='*', default=[], help='items to be added to the project configuration, specified in the format key:value')
    parser.add_argument('-v', '--version', action='version', help='show program version and exit', version='%(prog)s ' + __version__)

    # CLI values & config merge
    args = parser.parse_args()
    for pair in args.config:
        k, v = tokenize_kv(pair)
        cfg[k] = v
    cfg['project_name'] = args.project_name
    if args.project_type is not None:
        cfg['project_type'] = args.project_type

    # Validate finalized config
    if 'project_type' not in cfg.keys():
        die('missing required value: project_type')

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
        project.make(load_location, dump_location, tmap)
    except LoaderError as e:
        die('load error: {}'.format(e))
    except TransformerError as e:
        die('transform error: {}'.format(e))
    except DumperError as e:
        die('dump error: {}'.format(e))

    return 0
