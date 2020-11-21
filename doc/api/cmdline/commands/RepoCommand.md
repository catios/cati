Module cmdline.commands.RepoCommand
===================================
Repo command

Classes
-------

`RepoCommand()`
:   Repo command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   manage repositories
        
        Usage: cati repos [options]
        
        Options:
        -e|--edit: open repositories config file with editor
        -a|--add [new-repo]: add new repository
        
        Repo config structure:
        <url> pkg=<type of packages. for example `cati` or `deb`> arch=<wanted architecture> name=<an name for repo> priority=<priority between another repos>

    `run(self)`
    :   Run command