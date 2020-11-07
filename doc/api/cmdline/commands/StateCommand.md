Module cmdline.commands.StateCommand
====================================
State command

Classes
-------

`StateCommand()`
:   State command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   manage transactions state
        Options:
        --abort: cancel undoned transactions
        --complete: complete undoned transactions
        -y|--yes: do not ask for user confirmation

    `run(self)`
    :   Run command