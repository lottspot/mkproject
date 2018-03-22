# mkproject

Yet another project scaffolding tool

## Quick start

#### Install CLI tool

`mkproject` requires python 3. There are two installation method choices:

Compile and install the self-contained binary
```
make
sudo cp dist/mkproject /usr/local/bin/mkproject
```

Traditional install method
```
pip install .
```

The self-contained binary no longer depends on the
python interpreter after it has been built, but it
cannot be imported or used from other programs
as a traditionally installed python package can.

#### Install asset pack

The CLI tool will search for asset packs in `$HOME/.mkproject/assets`.
You can download an already existing asset pack and install it there
or create your own. The name of an asset pack corresponds to the
`PROJECT_TYPE` CLI parameter

#### Usage

```
usage: mkproject [-h] [-d DUMP_LOCATION] [-t PROJECT_TYPE] [-v]
                 project_name [config [config ...]]

positional arguments:
  project_name          name of the new project
  config                items to be added to the project configuration,
                        specified in the format key:value

optional arguments:
  -h, --help            show this help message and exit
  -d DUMP_LOCATION, --directory DUMP_LOCATION
                        directory to output project files into
  -t PROJECT_TYPE, --type PROJECT_TYPE
                        name of the project type to source templates from
  -v, --version         show program version and exit
```

