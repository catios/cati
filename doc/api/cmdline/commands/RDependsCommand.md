Module cmdline.commands.RDependsCommand
=======================================
RDepends command

Classes
-------

`RDependsCommand()`
:   RDepends command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   shows reverse depends list of packages
        
        this command shows which packages has dependency to an package
        
        Usage:
        - cati rdepends pkg1
        - cati rdepends pkg1 pkg2 ...

    `run(self)`
    :   Run command