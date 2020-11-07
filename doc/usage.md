# Cati usage
to learn cati usage, read this file.

## Options
- `-v|--version`: shows cati version
- `--no-ansi`: disable terminal ansi colors
- `--help`: shows help for a command. example: `cati list --help` shows help of list command
- `-q|--quiet`: quiet output
- `-v|--verbose`: verbose output

## help command
this command shows help:

```bash
cati help
```

also you can see help of a specify command:

```bash
cati help list
cati help remove
# ...
```

## pkg command
this command is for working with `.cati` packages.

#### pkg show
```bash
# showing packages
cati pkg show somepackage.cati
cati pkg show pkg1.cati /path/to/pkg2.cati # ...
```

Options:
- `--files|-f`: shows list of package files

#### pkg build
```bash
# building packages
cati pkg build package-dir/
cati pkg build package-dir1/ package-dir2/ # ...
```

Options:
- `--output|-o`: set package package output path. for example `cati pkg build pkg/ --output=package.cati`

#### pkg install
```bash
# installing packages
sudo cati pkg install somepackage.cati
sudo cati pkg install pkg1.cati pkg2.cati # ...
```

Options:
- `--without-scripts`: do not run package scripts in installation process

## list command
this command shows list of packages

```bash
cati list
```

Options:
- `--installed`: only show installed packages list
- `--installed-manual`: only show manual installed packages list
- `-q|--quiet`: quiet output, only show package names
- `--author`: filter packages list by author name. `--author='name of wanted author'` or more than 1 author: `--author='author 1 | author 2 | author 3'` (split with '|')
- `--maintainer`: filter packages list by maintainer name. `--maintainer='name of wanted maintainer'` or more than 1 author: `--maintainer='maintainer 1 | maintainer 2 | maintainer 3'` (split with '|')
- `--category`: filter packages list by category name. `--category='name of wanted category'` or more than 1 category: `--category='category 1 | category 2 | category 3'` (split with '|')

## remove command
this command remove packages

```bash
cati remove pkg1
cati remove pkg1 pkg2 # ...
```

Options:
- `-y|--yes`: do not ask for user confirmation
- `--conffiles`: also remove config files (full remove)
- `--without-scripts`: do not run package scripts in remove process

## show command
this command shows packages details

```bash
cati show somepackage
cati show pkg1 pkg2 # ...
```

Options:
- `--versions`: shows versions list of packages

## state command
this command is for managing state transactions. read [state system](/doc/developer/state-system.md) documentation.

```bash
cati state
cati state --abort
cati state --complete
```

Options:
- `--abort`: cancel undoned transactions
- `--complete`: complete undoned transactions (this option is in progress)

## query command
this command checks package query

for example:

```bash
cati query "somepackage >= 2.0"
cati query "somepackage = 1.7 | tstpkg & anotherpkg <= 1.5"
# ...
```
