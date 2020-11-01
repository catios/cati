Module dotcati.ArchiveModel
===========================
.cati package file model

Functions
---------

    
`archive_factory(file_path: str, type_str: str)`
:   Archive model factory.
    
    the strcuture of packages, maybe change in new version of cati.
    so, cati should be compatible with old packages where
    created with old version of cati. this class
    is a factory to check package version and
    return archive model object by that
    version.

Classes
-------

`ArchiveModelV1(file_path: str, type_str: str)`
:   .cati package file model (v1.0)

    ### Ancestors (in MRO)

    * dotcati.ArchiveModel.BaseArchive
    * package.Pkg.Pkg

`BaseArchive(file_path: str, type_str: str)`
:   base archive for archive versions

    ### Ancestors (in MRO)

    * package.Pkg.Pkg

    ### Descendants

    * dotcati.ArchiveModel.ArchiveModelV1

    ### Methods

    `add(self, path, arcname=None)`
    :   Add a file to package archive

    `close(self)`
    :   Close package archive

    `extractall(self, path)`
    :   Extract all of package files to `path`

    `info(self) ‑> dict`
    :   Returns package data.json information

    `members(self)`
    :   Returns members of the archive

    `pkg_version(self) ‑> str`
    :   Returns dotcati package strcuture version

    `read(self)`
    :   Load package information on object