Module cmdline.commands.ClearCacheCommand
=========================================
ClearCache command

Classes
-------

`ClearCacheCommand()`
:   ClearCache command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   clears cache files
        
        Usage: sudo cati clear-cache [options]
        
        Options:
        -v|--verbose: verbose output

    `run(self)`
    :   Run command