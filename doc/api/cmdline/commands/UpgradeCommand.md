Module cmdline.commands.UpgradeCommand
======================================
Upgrade command

Classes
-------

`UpgradeCommand()`
:   Upgrade command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   upgrade all of packages
        
        Usage: sudo cati upgrade [options]
        
        Options: all of `install` command options

    `run(self)`
    :   Run command