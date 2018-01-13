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
	rm -rf dist build *.spec

.PHONY: clean
