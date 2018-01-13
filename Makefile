BIN_PYINSTALLER := .env/bin/pyinstaller

PROG := mksaltformula
MAIN := $(PROG)/__init__.py
SRCS := \
  $(MAIN)

dist/$(PROG): $(SRCS)
	$(BIN_PYINSTALLER)  \
 --onefile                  \
 --name $(PROG)             \
 $(MAIN)

clean:
	rm -rf dist build *.spec *.egg-info
	find . -name __pycache__ -print0 | xargs -0 rm -rf

.PHONY: clean
