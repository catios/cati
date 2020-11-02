Module package.Pkg
==================
Package model

Classes
-------

`Pkg(data: dict)`
:   Package model

    ### Descendants

    * dotcati.ArchiveModel.BaseArchive

    ### Static methods

    `all_list()`
    :   Returns list of packages

    `compare_version(a, b)`
    :   Compares two versions.
        if 1 is returned means a is upper than b.
        if 0 is returned means a equals b.
        if -1 is returned means a is less than b.

    `get_last_version(versions: list)`
    :   Gets a list from versions and returns latest version in that list

    `installed_list()`
    :   Returns list of only installed packages

    `installed_version(package_name: str)`
    :   Gets name of package and returns installed version of that

    `is_installed(package_name: str)`
    :   Gets a package name and checks is installed or not

    `is_installed_manual(package_name: str)`
    :   Gets a package name and checks is installed MANUAL or not

    `load_from_index(index_json: dict, package_name: str)`
    :   Loads package data from index file

    `load_last(pkg_name: str)`
    :   Load last version of package by name

    `load_version(pkg_name: str, version: str)`
    :   loads a specify version of a package
        Outputs:
        - 1: package not found
        - 2: package found, but version not found
        - Pkg object: package and version found and returned

    ### Methods

    `check_state(query_string: str, virtual=None) ‑> bool`
    :   Checks package state by query string.
        
        For examples:
        "somepackage >= 1.5",
        "somepackage",
        "somepackage = 2.0",
        "somepackage < 1.7",
        "pkga | pkgb >= 1.0",
        "pkga | pkgb | pkgc",
        "pkga | pkgb & pkgc = 1.0",
        
        `virtual` argument:
        
        this argument can make a virtual package state
        for example package `testpkgz` is not installed,
        but we want to check the query when this is installed
        we can set that package in virtual system to query checker
        calculate tha package as installed/removed
        virtual structure: this is dictonary:
        {
            'install': [
                ## a list from installed packages:
                ['testpkgx', '1.0'],
                ['testpkgz', '3.7.11'],
                ...
            ]
        }

    `get_conffiles(self)`
    :   Returns package conffiles list

    `get_conflicts(self)`
    :   Returns package conflicts list

    `get_depends(self)`
    :   Returns package dependencies list

    `get_reverse_conflicts(self) ‑> list`
    :   Returns list of packages has conflicts with this package

    `get_reverse_depends(self) ‑> list`
    :   Returns list of packages has dependency to this package

    `get_versions_list(self)`
    :   returns versions list of the package
        Output structure: list [ [<version>, <arch>] ]

    `installed(self)`
    :   Checks current package is installed. if yes, returns installed version and if not, returns False