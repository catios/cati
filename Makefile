SHELL = bash

.DEFAULT_GOAL := main
.PHONY := headers compile clean pylint test main all

PY = python3
MANAGE = $(PY) ./manage.py
PYINSTALLER = $(PY) $(shell which pyinstaller)

PYINSTALLER_IS_INSTALLED = 0
ifneq (,$(shell command -v pyinstaller))
PYINSTALLER_IS_INSTALLED = 1
endif

GIT_IS_INSTALLED = 0
ifneq (,$(shell command -v git))
GIT_IS_INSTALLED = 1
endif

PYLINT_IS_INSTALLED = 0
ifneq (,$(shell command -v pylint3))
PYLINT_IS_INSTALLED = 1
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

pylint:
ifeq (1,$(PYLINT_IS_INSTALLED))
	-@pylint3 $(shell find src -type f -name "*.py") | grep -v "(invalid-name)" > pylint.out
else
	@echo -e "\033[32mpylint3 is not installed\033[0m"
endif

test:
	$(PY) tests/run.py

all: headers test
ifeq (1,$(GIT_IS_INSTALLED))
	-@git status
endif
