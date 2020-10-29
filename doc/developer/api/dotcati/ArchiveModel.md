Module dotcati.ArchiveModel
===========================
.cati package file model

Classes
-------

`ArchiveModel(file_path: str, type_str: str)`
:   .cati package file model

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