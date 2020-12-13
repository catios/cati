Module cmdline.commands.FinfoCommand
====================================
Finfo command

Classes
-------

`FinfoCommand()`
:   Finfo command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   shows info about an file
        
        this command says an file is for which package and some another details
        
        Usage: cati finfo /path/to/file

    `run(self)`
    :   Run command