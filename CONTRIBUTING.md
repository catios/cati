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
before start, you need to install cati dev-dependencies:
- `python3 (>= 3.6)`
- `pip3`
- `virtualenv`
- `make`

to check them you can use the following commands:

```bash
python3 --version
python3 -m pip --version
virtualenv --version
make --version
```

next, to start development environment, do the following steps:

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
python3 cati
# OR
./cati/__main__.py
```

every thing is ready for coding!

## branch
also send pull requests to `master` branch.

## commit message
try to write commit messages in this pattern: `<section>: <details>`.

for example: `cmdline: fix a bug in help command`
or `remover: add new features to remover`
and ...

## testing
if you are adding/changing a feature, sync test of that feature with your changes (read [testing guide](/doc/developer/testing.md)).

## docstring
make sure to writing good docstring for classes, functions and variables.
write docstring between `"""` (double qoute, not single qoute).

Also use [google python docstring style](https://google.github.io/styleguide/pyguide.html#s3.8.1-comments-in-doc-strings) to writing docstrings.

## always run `make all`
always run `make all` command after your changes.

## idea
if you don't have any idea and want to contribute, best way to find tasks is that to check [issues](https://github.com/catios/cati/issues) and [todo](/TODO.md) file.
