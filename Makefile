SHELL = bash

.DEFAULT_GOAL := main
.PHONY := headers compile clean main all

PY = python3
MANAGE = $(PY) ./manage.py
PYINSTALLER = $(PY) $(shell which pyinstaller)

PYINSTALLER_IS_INSTALLED = 0
ifneq (,$(shell command -v pyinstaller))
PYINSTALLER_IS_INSTALLED = 1
endif

headers:
	@$(MANAGE) update-headers
	@echo -e "\033[32mCode copyright headers updated successfuly\033[0m"

compile:
ifeq (1,$(PYINSTALLER_IS_INSTALLED))
	@$(PYINSTALLER) src/cati.py --onefile
else
	@echo -e "\033[31mPyinstaller is not installed\033[0m"
endif

clean:
	@rm dist/ build/ *.spec -rf
	@echo -e "\033[32mall of build files cleared successfuly\033[0m"

main: compile

all: headers
