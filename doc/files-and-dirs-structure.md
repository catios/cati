# Cati files and directories structure

## directory `/var/lib/cati/lists`

this directory keeps list of packages.

for example:

```
/var/lib/cati/lists/somepackage/
```

there is one directory for one package

in package list directory:

```bash
/var/lib/cati/lists/somepackage/:
index # a file to keep list of versions of this package
1.0-amd64
1.0-all
1.2-i386
1.2-amd64
2.0-all
# ...
```

there is a file for versions of packages.
for example, `somepackage` with version `1.5` for `amd64` architecture, has a file in
`/var/lib/cati/lists/somepackage/1.5-amd64`. this file keeps information of this package.

also there is a file named `/var/lib/cati/lists/somepackage/index`.
the `index` file just keeps list of versions and architectures of package.

## directory `/var/lib/cati/installed`
this directory contains list of INSTALLED packages.

for example, package `somepackage` is installed. there is a directory named `/var/lib/cati/installed/somepackage/`.
in this directory, is some files:
- `ver`: contains installed version of package
- `files`: contains list of package installed files on system
- `staticfiles`: contains list of package installed STATIC files and hash of them
- `installed_at`: contains time where package installed at that time
- `manual`: this file is optional. if this file exists, means this package is installed manually

so, there is this files for `somepackage` installation: `/var/lib/cati/installed/somepackage/ver`, `/var/lib/cati/installed/somepackage/files`, `/var/lib/cati/installed/somepackage/installed_at`

## directory `/var/lib/cati/any-scripts`
this directory keeps list of packages `any` scripts.

packages has an script named `any`. cati keeps them in this folder.
for example any script of package `pkg1` is saved in `/var/lib/cati/any-scripts/pkg1`

## directory `/var/lib/cati/security-blacklist`
this directory keeps security blacklist database.

read [security blacklist system](/doc/security-blacklist.md).

## file `/var/lib/cati/state.f`
this file contains transaction state.
read [State system](/doc/developer/state-system.md)

## file `/var/lib/cati/unremoved-conffiles.list`
this file contains list of unremoved config files of packages to handle then later.

## file `/etc/cati/repos.list`
this file contains list of repositories

read [repository system](/doc/repositories.md).

## directory `/etc/cati/repos.list.d`
this directory contains list of repositories in parted files.

read [repository system](/doc/repositories.md).

## directory `/var/cache/cati`
cati uses this directory to cache some data like downloaded archives and repositories downloaded data.
