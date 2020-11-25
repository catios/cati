Module cmdline.commands.InstallCommand
======================================
Install command

Classes
-------

`InstallCommand()`
:   Install command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   install packages
        
        Usage: cati install [options] pkg1 pkg2 pkg3 ...
        ...... cati install [options] pkg1 pkg2=<version> ...
        
        Options:
        -y|--yes: don't ask for user confirmation

    `run(self)`
    :   Run command