Module cati.dotcati.PackageJsonValidator
========================================
Package information json validator

Classes
-------

`PackageJsonValidator()`
:   Package information json validator

    ### Static methods

    `validate(data: dict) ‑> bool`
    :   This function gets a json object and checks that fields and value of them where
        are required for a valid package data.json and says this data
        is valid or not
        
        Args:
            data: package data.json as dictonary
        
        Returns:
            boolean. True means data is valid and False means data is invalid