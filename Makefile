SHELL = bash

.DEFAULT_GOAL := main
.PHONY := headers compile clean pylint test main all

PY = python3
MANAGE = $(PY) ./manage.py

GIT_IS_INSTALLED = 0
ifneq (,$(shell command -v git))
GIT_IS_INSTALLED = 1
endif

### headers		update codes copyright headers
headers:
	@$(MANAGE) update-headers
	@echo -e "\033[32mCode copyright headers updated successfuly\033[0m"

### compile		compile program with pyinstaller
compile:
	@$(PY) -m PyInstaller src/cati.py --onefile

### clean		clear build files
clean:
	@rm dist/ build/ *.spec -rf
	@echo -e "\033[32mall of build files cleared successfuly\033[0m"

main: compile

### pylint		check code with pylint
pylint:
	@$(PY) -m pylint $(shell find src -type f -name "*.py") | grep -v "(invalid-name)" > pylint.out

### test		run tests
test:
	@echo ''
	@$(PY) tests/run.py
	@echo ''

### help		shows this help
help:
	@echo 'Makefile commands:'
	@cat $(shell pwd)/Makefile | grep '###' | grep -v '@cat'

### all			do all of actions
all: headers test
ifeq (1,$(GIT_IS_INSTALLED))
	-@git status
endif
