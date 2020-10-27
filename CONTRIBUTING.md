# Contributing to cati

#### NOTE: surely read [documentation](/doc) before contributing

## start contributing

if you want to start contributing to cati, do the following steps:
- fork project
- clone your fork
- create a branch and checkout to that branch
- make your changes and commit
- push your branch to your fork
- send pull request from your branch to `master`

### run/build

to start development environment, do the following steps:

```bash
git clone <your-fork-url>
cd cati

# create virtual env with virtualenv
virtualenv venv -p python3
source venv/bin/activate

# install dependencies
pip3 install -r requirements.txt

# make all
make all

# run for test
./src/cati.py
```

every thing is ready!

## branch
also send pull requests to `master` branch.

## commit message
try to write commit messages in this pattern: `<section>: <details>`.

for example: `cmdline: fix a bug in help command`
or `remover: add new features to remover`
and ...

## testing
if you are adding/changing a feature, sync test of that feature with your changes (read [testing guide](/doc/developer/testing.md)).

## always run `make all`
always run `make all` command after your changes.

## idea
if you don't have any idea and want to contribute, best way to find tasks is that to check [issues](https://github.com/parsampsh/cati/issues) and [todo](/TODO.md) file.

