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
        
        Returns:
            dict: output has two keys:
                  {
                      "list": list[Pkg] // list of packages
                      "errors": list // errors while loading packages
                  }

    `compare_version(a: str, b: str)`
    :   Compares two versions.
        
        Args:
            a (str): first version
            b (str): second version
        
        Returns:
            if 1 is returned means a is upper than b.
            if 0 is returned means a equals b.
            if -1 is returned means a is less than b.

    `get_all_installed_files_list() ‑> list`
    :   returns list of all of installed files
        
        Returns:
            list: [
                ['pkgname', 'filetype(d,f,cd,cf)', '/file/path'],
                ['pkg1', 'f', '/path/to/file'],
                ...
            ]

    `get_download_size_str(dsize: int) ‑> str`
    :   Returns file size str from bytes interger
        
        Args:
            dsize: bytes count
        
        Returns:
            str: download str

    `get_last_version(versions: list) ‑> str`
    :   Gets a list from versions and returns latest version in that list
        
        Args:
            versions (list[str]): list of versions you want find last of them
        
        Returns:
            str: the last version in the list

    `installed_list() ‑> dict`
    :   Returns list of only installed packages 
        
        Returns:
            dict: output has two keys:
                  {
                      "list": list[Pkg] // list of packages
                      "errors": list // errors while loading packages
                  }

    `installed_version(package_name: str) ‑> str`
    :   Gets name of package and returns installed version of that
        
        Args:
            package_name (str): name of package
        
        Returns:
            str: installed version
        
        Raises:
            package.exceptions.CannotReadFileException: when cannot read package database files

    `is_installed(package_name: str) ‑> bool`
    :   Gets a package name and checks is installed or not
        
        Args:
            package_name (str): the package name you want to check is installed
        
        Returns:
            bool

    `is_installed_manual(package_name: str) ‑> bool`
    :   Gets a package name and checks is installed MANUAL or not
        
        Args:
            package_name (str): the package name you want to check is installed
        
        Returns:
            bool

    `load_from_index(index_json: dict, package_name: str)`
    :   Loads package data from index file
        
        Args:
            package_name (str): name of the package
            index_json (dict): loaded json data from `/var/lib/cati/lists/<pkgname>/index` file
        
        Returns:
            Pkg: the loaded Pkg object

    `load_last(pkg_name: str) ‑> bool`
    :   Load last version of package by name
        
        Args:
            pkg_name (str): the package name
        
        Returns:
            bool (False): package not found
            Pkg: the loaded Pkg boject

    `load_version(pkg_name: str, version: str, arch='')`
    :   loads a specify version of a package
        
        Args:
            pkg_name (str): name of package
            version (str): that version you want to load
            arch (str): load specify arch (optional)
        
        Returns:
            int (1): package not found
            int (2): package found, but version/arch not found
            Pkg object: package and version found and returned

    ### Methods

    `check_state(query_string: str, virtual=None, get_false_pkg=False, get_false_pkg_next=0, get_true_pkg=False, get_true_pkg_next=0, only_parse=False) ‑> bool`
    :   Checks package state by query string.
        
        Examples:
        "somepackage >= 1.5",
        "somepackage",
        "somepackage = 2.0",
        "somepackage < 1.7",
        "pkga | pkgb >= 1.0",
        "pkga | pkgb | pkgc",
        "pkga | pkgb & pkgc = 1.0",
        
        also there is a feature to check files:
        
        "@/usr/bin/somefile",
        "somepackage | @/path/to/somefile",
        "testpkga >= 3.0 | @/somefile"
        "@/file/one | @/file/two",
        "@<sha256-hash>@/path/to/file",
        "@76883f0fd14015c93296f0e4202241f4eb3a23189dbc17990a197477f1dc441a@/path/to/file"
        
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
        
            'remove': [
                ## a list from removed packages:
                ['testpkgx', '1.0'],
                ['testpkgz', '3.7.11'],
                ...
            ]
        
            ## set it True if you want to ignore real installations
            'no_real_installs': True/False
        
            ## set it True if you want to ignore real not installations
            'all_real_is_installed': True/False
        }

    `get_conffiles(self) ‑> list`
    :   Returns package conffiles list

    `get_conflicts(self) ‑> list`
    :   Returns package conflicts list

    `get_depends(self) ‑> list`
    :   Returns package dependencies list

    `get_file_size_str(self) ‑> str`
    :   Returns file size of the package as str (for example `32 MB`)
        
        Returns:
            str: file size str

    `get_recommends(self) ‑> list`
    :   Returns package recommends list

    `get_replaces(self) ‑> list`
    :   Returns package replaces list

    `get_reverse_conflicts(self) ‑> list`
    :   Returns list of packages has conflicts with this package
        
        Returns:
            list[Pkg]: list of packages has conflict with this package

    `get_reverse_depends(self) ‑> list`
    :   Returns list of packages has dependency to this package
        
        Returns:
            list[Pkg]: list of packages has dependency to this package

    `get_static_files(self) ‑> list`
    :   returns package static files list

    `get_versions_list(self)`
    :   returns versions list of the package
        
        Returns:
            list: list of versions: [ [<version>, <arch>] ]

    `installed(self) ‑> (<class 'str'>, <class 'bool'>)`
    :   Checks current package is installed. if yes, returns installed version and if not, returns False

    `installed_static_files(self) ‑> list`
    :   returns list of installed files of package
        
        Returns:
            list[str]: files paths