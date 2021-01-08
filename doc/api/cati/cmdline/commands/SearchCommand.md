Module cati.cmdline.commands.SearchCommand
==========================================
Search command

Classes
-------

`SearchCommand()`
:   Search command

    ### Ancestors (in MRO)

    * cati.cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   search between packages by name and description
        
        (this command is a alias for `cati list --search='word'`)
        
        Usage: cati search 'word'

    `run(self)`
    :   Run command