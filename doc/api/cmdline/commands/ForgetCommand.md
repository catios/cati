Module cmdline.commands.ForgetCommand
=====================================
Forget command

Classes
-------

`ForgetCommand()`
:   Forget command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `empty_method_for_event(a=None, b=None)`
    :   an empty method

    `help(self)`
    :   forgets packages from packages list
        
        Usage: cati forget pkg1 pkg2 pkg3=1.6.7 ...

    `run(self)`
    :   Run command