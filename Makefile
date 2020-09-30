.DEFAULT_GOAL := main
.PHONY := headers

PY = python3
MANAGE = $(PY) ./manage.py
PYINSTALLER = $(PY) $(shell which pyinstaller)

headers:
	@$(MANAGE) update-headers

compile:
	@$(PYINSTALLER) src/cati.py --onefile

main: compile
