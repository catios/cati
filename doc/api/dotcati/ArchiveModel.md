Module dotcati.ArchiveModel
===========================
.cati package file model

Classes
-------

`ArchiveModel(file_path: str, type_str: str)`
:   Archive model factory.
    
    the strcuture of packages, maybe change in new version of cati.
    so, cati should be compatible with old packages where
    created with old version of cati. this class
    is a factory to check package version and
    return archive model object by that
    version.

`ArchiveModelV1(file_path: str, type_str: str)`
:   .cati package file model (v1.0)

    ### Methods

    `add(self, path, arcname=None)`
    :   Add a file to package archive

    `close(self)`
    :   Close package archive

    `extractall(self, path)`
    :   Extract all of package files to `path`

    `get_conflicts(self)`
    :   Returns package conflicts list

    `get_depends(self)`
    :   Returns package dependencies list

    `info(self) ‑> dict`
    :   Returns package data.json information

    `members(self)`
    :   Returns members of the archive

    `pkg_version(self) ‑> str`
    :   Returns dotcati package strcuture version

    `read(self)`
    :   Load package information on object