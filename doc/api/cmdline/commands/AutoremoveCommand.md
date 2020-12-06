Module cmdline.commands.AutoremoveCommand
=========================================
Autoremove command

Classes
-------

`AutoremoveCommand()`
:   Autoremove command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `find_unused_packages(self)`
    :   finds unused packages

    `help(self)`
    :   remove unused automaticaly installed packages
        
        Usage: sudo cati autoremove [options]
        
        Options: all of remove command options

    `run(self)`
    :   Run command