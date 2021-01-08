Module cati.transaction.runners.Remove
======================================
Remove transaction

Classes
-------

`Remove()`
:   Remove transaction

    ### Ancestors (in MRO)

    * cati.transaction.BaseTransaction.BaseTransaction

    ### Static methods

    `add_to_unremoved_conffiles(pkg: cati.package.Pkg.Pkg, filepath: str)`
    :   Adds filepath to list of unremoved conffiles

    `run(pkg: cati.package.Pkg.Pkg, events: dict, remove_conffiles=False, run_scripts=True)`
    :   Remove pkg