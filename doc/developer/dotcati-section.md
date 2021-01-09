# Dotcati section
this document is for `cati/dotcati` section.

## archive_factory
this function is factory to load `.cati` file object.

```python
# ...

from cati.dotcati.ArchiveModel import archive_factory

pkg = archive_factory('/path/to/package.cati', 'r') # first argument is file path and second argument is open type

# ...
```

you can see another functions of archive model in `cati/dotcati/ArchiveModel.py`

## Builder
this class is dotcati package builder.

```python
# ...

from cati.dotcati.Builder import Builder

builder = Builder()
output = builder.build('/path/to/package/dir')
# output is created package path
# also you can pass second argument as output file path to specify output path
output = builder.build('/path/to/package/dir', 'package.cati')

# ...
```

## PackageJsonValidator
this module gets package information as json (`data.json`) and validate fields in that.

```python
# ...

from cati.dotcati.PackageJsonValidator import PackageJsonValidator

PackageJsonValidator.validate(data) # output is boolean

# ...
```

## ListUpdater
this module updates `index` files in package lists (read [Files and dirs structure](/doc/files-and-dirs-structure.md)).

this module loads list of versions of a package and list them and put created list to package list index file.

```python
# ...

from cati.dotcati.ListUpdater import ListUpdater

ListUpdater.update_indexes(events)

# ...
```

also `update_indexes` function has a argument named `events` (read [Event pattern](/doc/developer/event-pattern.md)). read docstring of this function to know events of this function

## Installer
this module installs a dotcati package.

```python
# ...

from cati.dotcati.Installer import Installer

installer = Installer()
installer.install(pkg_archive, index_updater_events={}, installer_events={})

# ...
```

the `install` function gets two events list argument named `index_updater_events` and `installer_events`. read function docstring to know that events.
