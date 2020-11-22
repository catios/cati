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
        
        Usage: cati autoremove [options]
        
        Options:
        -y|--yes: do not ask for user confirmation
        --conffiles: also remove conffiles (full remove)
        --without-scripts: do not run package scripts in remove process

    `run(self)`
    :   Run command