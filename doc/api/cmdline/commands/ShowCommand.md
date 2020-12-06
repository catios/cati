Module cmdline.commands.ShowCommand
===================================
Show command

Classes
-------

`ShowCommand()`
:   Show command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   shows details of packages
        
        Usage: cati show pkg1 pkg2 ... [options]
        
        Options:
        --versions: shows versions list of packages

    `run(self)`
    :   Run command