# Cati command line usage
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

Usage: `cati pkg [subcommand] [args] [options]`

Subcommands:
- `build`:      build .cati package from directory(s)
- `show`:       show content of .cati package(s). options: --files: show package files
- `install`:    install a .cati package on system

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
- `--output=[path]|-o=[path]`: set package package output path

#### pkg install
```bash
# installing packages
sudo cati pkg install somepackage.cati
sudo cati pkg install pkg1.cati pkg2.cati # ...
```

Options:
- `--without-scripts`: do not run package scripts in installation process
- `--keep-conffiles`: don't overwrite new version of config files
- `--target=[files-install-location-prefix-path]`: set files installation prefix

## list command
this command shows list of packages

```bash
cati list
```

Options:
- `--installed`: show only installed packages
- `--installed-manual`: show only manual installed packages
- `--author=[author-name or author-nameS splited by '|']`: filter packages list by author name
- `--maintainer=[maintainer-name or author-nameS splited by '|']`: filter packages list by maintainer name
- `--category=[category-name or category-nameS splited by '|']`: filter packages list by category
- `--search=[word]`: search by packages name and description
- `--upgradable`: show list of upgradable

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
- `--complete`: complete undoned transactions

## query command
this command checks package query

for example:

```bash
cati query "somepackage >= 2.0"
cati query "somepackage = 1.7 | tstpkg & anotherpkg <= 1.5"
# ...
```

read [package query guide](package-query.md) for more information.

## search command
search between packages by name and description (is alias of `cati list --search="someword"`)

```bash
cati search 'someword'
```

## files command
shows list of package files

Options:
- `--installed`: shows list of all of installed files/dirs

```bash
cati files somepkg
cati files pkg1 pkg2 # ...
cati files --installed
```

## finfo command
shows info about an file

```bash
cati finfo /usr/bin/somefile
cati finfo ../dir/file
```

this info contains that which package is owner of the file and type of that file (conffile)

## rdepends command
shows reverse depends list of packages (list of that packages has dependency to a package)

```bash
cati rdepends pkg1
cati rdepends pkg1 pkg2 # ...
cati rdepends pkg1 --quiet # quiet output
```

## forget command
forgets packages from packages list

```bash
cati forget pkg1
cati forget pkg1=1.12.7 # only version 1.12.7
cati forget pkg1 pkg2 pkg3=1.0 pkg4
```

## check command
checks system health and packages security

this command checks system health and packages security and static files

```bash
cati check
```

## repo command
manage repositories

Options:
- `-a|--add [new repo]`: add new repository
- `-e|--edit`: open repositories config file with vim editor
- `--scan [repository directory]`: scan packages inside an directory and create data files from package to make that dir an local repository

```bash
cati repo
sudo cati repo --edit
sudo cati repo --add '<new repo>'
cati repo --scan /path/to/packages/dir
```

read [repositories guide](/doc/repositories.md) for more information about repositories.

## update command
update list of available packages from repositories

```bash
sudo cati update
```

## autoremove command
remove unused automatic installed packages.

Options:
- `-y|--yes`: do not ask for user confirmation
- `--conffiles`: also remove config files (full remove)
- `--without-scripts`: do not run package scripts in remove process

```bash
sudo cati autoremove [options]
```

## clear-cache command
clears cache files

```bash
cati clear-cache
```

## download command
download packages

Options:
- `--output=[file output path]`: set file output path

```bash
cati download pkg1
cati download pkg1=<version> pkg2=<version>
cati download pkg1=<version>=<arch>
cati download pkg1 --output=a.cati
```

## install command
install packages

Options:
- `-y|--yes`: don't ask for user confirmation
- `--reinstall`: re-install currently installed packages
- `--download-only`: only download packages. this helps you to only download packages and install them later

```bash
sudo cati install [options] pkg1 pkg2 pkg3 ...
sudo cati install [options] pkg1 pkg2=<version>
sudo cati install somepkg --reinstall # reinstall somepkg if currently installed
```

## upgrade command
upgrade all of packages

Options: all of `install` command options

```bash
sudo cati upgrade [options]
```

## full-upgrade command
update, upgrade and autoremove

Options:
- `-y|--yes`: don't ask for user confirmation

```bash
sudo cati full-upgrade [options]
```
