PROG := mksaltformula
MAIN := $(PROG)/__init__.py
SRCS := \
  $(MAIN)

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
	rm -rf dist build .env *.spec *.egg-info
	find . -name __pycache__ -print0 | xargs -0 rm -rf

.PHONY: clean env test
