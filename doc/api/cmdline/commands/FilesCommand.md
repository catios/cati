Module cmdline.commands.FilesCommand
====================================
Files command

Classes
-------

`FilesCommand()`
:   Files command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   shows files list of packages
        
        Usage:
        - cati files pkg1
        - cati files pkg1 pkg2 ...
        
        Options:
        --installed: shows list of all of installed files/dirs

    `run(self)`
    :   Run command