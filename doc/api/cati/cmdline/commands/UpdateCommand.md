Module cati.cmdline.commands.UpdateCommand
==========================================
Update command

Classes
-------

`UpdateCommand()`
:   Update command

    ### Ancestors (in MRO)

    * cati.cmdline.BaseCommand.BaseCommand

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
        
        Options:
        -q|--quiet: quiet output
        -v|--verbose: verbose output

    `run(self)`
    :   Run command