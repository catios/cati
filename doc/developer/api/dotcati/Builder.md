Module dotcati.Builder
======================
Cati package builder

Classes
-------

`Builder()`
:   Cati package builder

    ### Static methods

    `json_fields_are_valid(data: dict)`
    :

    ### Methods

    `build(self, dirpath: str, output=None)`
    :   This function gets a directory and builds a .cati package from that
        the output is optional parameter. this argument can be used
        to set package output file.

    `compress(self, dirpath: str, output: str)`
    :   This function compresses content of target directory and build package
        in output file