PROG := mkproject
MAIN := $(PROG)/__main__.py
SRCS := \
  $(MAIN)                               \
  $(PROG)/__init__.py                   \
  $(PROG)/cli.py                        \
  $(PROG)/asset_pack.py                 \
  $(PROG)/loader/__init__.py            \
  $(PROG)/dumper/__init__.py            \
  $(PROG)/transformer/__init__.py       \
  $(PROG)/loader/search.py              \
  $(PROG)/loader/directory.py           \
  $(PROG)/dumper/fs.py                  \
  $(PROG)/transformer/template.py       \
  $(PROG)/transformer/path.py           \
  $(PROG)/transformer/mako.py

DIR_ENV         := .env
DIR_BIN         := $(DIR_ENV)/bin
BIN_PIP         := $(DIR_BIN)/pip
BIN_PYINSTALLER := $(DIR_BIN)/pyinstaller

python ?= python3

dist/$(PROG): $(SRCS) $(BIN_PYINSTALLER) $(DIR_BIN)/$(PROG)
	$(BIN_PYINSTALLER)  \
 --onefile                  \
 --name $(PROG)             \
 $(MAIN)

$(BIN_PYINSTALLER): $(BIN_PIP)
	$(BIN_PIP) install -r requirements.txt

$(DIR_BIN)/$(PROG): $(BIN_PIP)
	$(BIN_PIP) install .

$(BIN_PIP):
	$(python) -m venv $(DIR_ENV)

env: $(BIN_PYINSTALLER)

test: $(BIN_PIP)
	$(DIR_BIN)/python setup.py test

clean:
	rm -rf dist build .env *.spec *.egg-info .eggs
	find . -name __pycache__ -print0 | xargs -0 rm -rf
	find . -name '*.pyc' -print0 | xargs -0 rm -f

.PHONY: clean env test
