SHELL = bash

.DEFAULT_GOAL := main
.PHONY := headers compile install main clean pylint test all docs help

PY = python3
MANAGE = $(PY) ./manage.py
INSTALLATION_PATH = /usr/bin/cati

GIT_IS_INSTALLED = 0
ifneq (,$(shell command -v git))
GIT_IS_INSTALLED = 1
endif

### headers		update codes copyright headers
headers:
	@$(MANAGE) update-headers
	@echo -e "\033[32mCode copyright headers updated successfuly\033[0m"

### compile		compile program with pyinstaller
compile: all
	@PYTHONPATH='$(shell pwd)/src' $(PY) -m PyInstaller src/cati.py --onefile

### install		installs program on system
install: ./dist/cati
	@cp ./dist/cati $(INSTALLATION_PATH)
	@echo -e "\033[32mCati installed successfuly\033[0m"
	@$(INSTALLATION_PATH)

### clean		clear build files
clean:
	@rm dist/ build/ *.spec -rf
	@echo -e "\033[32mall of build files cleared successfuly\033[0m"

main: compile

### pylint		check code with pylint
pylint:
	@$(PY) -m pylint $(shell find src -type f -name "*.py") | grep -v "(invalid-name)" > pylint.out

### docs		generates api documentation
docs:
	@rm -rf doc/api
	@printf 'Generating api doc... '
	@PYTHONPATH='$(shell pwd)/src' $(PY) -m pdoc frontend package transaction cmdline repo helpers dotcati --output-dir doc/api --skip-errors &> /dev/null
	@printf '\033[32mFinished\033[0m\n'

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
all: headers docs test
ifeq (1,$(GIT_IS_INSTALLED))
	-@git status
endif
