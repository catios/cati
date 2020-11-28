Module dotcati.Builder
======================
Cati package builder

Classes
-------

`Builder()`
:   Cati package builder

    ### Static methods

    `json_fields_are_valid(data: dict) ‑> bool`
    :   alias for PackageJsonValidator.validate (validates package json info)
        
        Args:
            data: package data.json as dict
        
        Returns:
            returns boolean. True means json data is valid and False means invalid

    ### Methods

    `build(self, dirpath: str, output=None)`
    :   This function gets a directory and builds a .cati package from that.
        
        Args:
            dirpath: (str) package directory
            output: (str or None) path of the package output
        
        Raises:
            FileNotFoundError: when the directory not exists
            dotcati.exceptions.InvalidPackageDirException: when there is an probelm in package directory (problem will put as exception message)

    `compress(self, dirpath: str, output: str)`
    :   This function compresses content of target directory and build package
        in output file
        
        Args:
            dirpath: (str) package directory path
            output: (str) that filepath you want to compress file in that
        
        Raises:
            InvalidPackageDirException: when the output path is invalid