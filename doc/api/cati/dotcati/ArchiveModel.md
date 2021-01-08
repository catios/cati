Module cati.dotcati.ArchiveModel
================================
.cati package archive handling

Functions
---------

    
`archive_factory(file_path: str, type_str: str) ‑> cati.dotcati.ArchiveModel.BaseArchive`
:   Archive model factory. Loads a package archive from file
    
    the strcuture of packages, maybe change in new version of cati.
    so, cati should be compatible with old packages where
    created with old version of cati. this class
    is a factory to check package version and
    return archive model object by that
    version.
    
    Args:
        file_path: (str) archive filepath
        type_str: (str) open type of archive (r,w)
    
    Returns:
        returns instance of `dotcati.ArchiveModel.BaseArchive` as loaded package object

Classes
-------

`ArchiveModelV1(file_path: str, type_str: str)`
:   .cati package file model (v1.0)

    ### Ancestors (in MRO)

    * cati.dotcati.ArchiveModel.BaseArchive
    * cati.package.Pkg.Pkg

`BaseArchive(file_path: str, type_str: str)`
:   base archive for archive versions

    ### Ancestors (in MRO)

    * cati.package.Pkg.Pkg

    ### Descendants

    * cati.dotcati.ArchiveModel.ArchiveModelV1

    ### Methods

    `add(self, path: str, arcname=None)`
    :   Add a file to package archive (in `w` mode)
        
        Args:
            path: that file you want to add
            arcname: the arcname

    `close(self)`
    :   Close package archive

    `extractall(self, path: str)`
    :   Extract all of package files to `path` arg

    `info(self) ‑> (<class 'dict'>, None)`
    :   Returns package data.json information

    `members(self) ‑> list`
    :   Returns members of the archive as paths string
        
        Returns:
            list[str] list of path strings

    `pkg_version(self) ‑> str`
    :   Returns dotcati package strcuture version
        
        Returns:
            '1.0' str

    `read(self)`
    :   Load package information on object.
        
        This method has not arg or output, just loads some information of package to this object.
        
        Raises:
            Exception: will raise normal Exception when package json data is invalid
                       (validated by dotcati.PackageJsonValidator.validate())