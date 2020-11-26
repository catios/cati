Module cmdline.commands.UpdateCommand
=====================================
Update command

Classes
-------

`UpdateCommand()`
:   Update command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `download_event(self, url, output)`
    :   repo data download event

    `empty_method(self, a=None, b=None)`
    :   an empty method

    `help(self)`
    :   updates list of available packages from repositories
        
        Usage: cati update [options]

    `run(self)`
    :   Run command