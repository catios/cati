Module cmdline.commands.CheckCommand
====================================
Check command

Classes
-------

`CheckCommand()`
:   Check command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   checks system health and security
        
        this command checks system health and packages security and static files
        
        Usage: sudo cati check [options]
        
        Options:
        -q|--quiet: quiet output
        -v|--verbose: verbose output

    `run(self)`
    :   Run command