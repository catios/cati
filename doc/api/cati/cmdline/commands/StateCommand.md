Module cati.cmdline.commands.StateCommand
=========================================
State command

Classes
-------

`StateCommand()`
:   State command

    ### Ancestors (in MRO)

    * cati.cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   manage transactions state
        
        Usage: cati state [options]
        
        Options:
        --abort: cancel undoned transactions
        --complete: complete undoned transactions
        -y|--yes: do not ask for user confirmation

    `run(self)`
    :   Run command