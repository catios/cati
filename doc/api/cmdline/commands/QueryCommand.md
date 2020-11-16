Module cmdline.commands.QueryCommand
====================================
Query command

Classes
-------

`QueryCommand()`
:   Query command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   checks a package query
        
        Usage:
        - cati query [query]
        - cati query "somepackage >= 1.0"

    `run(self)`
    :   Run command