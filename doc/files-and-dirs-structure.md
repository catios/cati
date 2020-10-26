# Cati files and directories structure

## `/var/lib/cati/lists`

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

## `/var/lib/cati/installed`
this directory contains list of INSTALLED packages.

for example, package `somepackage` is installed. there is a directory named `/var/lib/cati/installed/somepackage/`.
in this directory, is some files:
- `ver`: contains installed version of package
- `files`: contains list of package installed files on system
- `installed_at`: contains time where package installed at that time

so, there is this files for `somepackage` installation: `/var/lib/cati/installed/somepackage/ver`, `/var/lib/cati/installed/somepackage/files`, `/var/lib/cati/installed/somepackage/installed_at`

## `/var/lib/cati/state.f`
this file contains transaction state.
read [State system](/doc/developer/state-system.md)
