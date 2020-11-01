Module transaction.runners.Remove
=================================
Remove transaction

Classes
-------

`Remove()`
:   Remove transaction

    ### Ancestors (in MRO)

    * transaction.BaseTransaction.BaseTransaction

    ### Static methods

    `add_to_unremoved_conffiles(pkg: package.Pkg.Pkg, filepath: str)`
    :   Adds filepath to list of unremoved conffiles

    `run(pkg: package.Pkg.Pkg, events: dict, remove_conffiles=False)`
    :   Remove pkg