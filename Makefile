.DEFAULT_GOAL := main
.PHONY := headers compile clean main

PY = python3
MANAGE = $(PY) ./manage.py
PYINSTALLER = $(PY) $(shell which pyinstaller)

headers:
	@$(MANAGE) update-headers

compile:
	@$(PYINSTALLER) src/cati.py --onefile

clean:
	@rm dist/ build/ *.spec -rf
	@echo all of build files cleared successfuly

main: compile
