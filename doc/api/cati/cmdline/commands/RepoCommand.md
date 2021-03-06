Module cati.cmdline.commands.RepoCommand
========================================
Repo command

Classes
-------

`RepoCommand()`
:   Repo command

    ### Ancestors (in MRO)

    * cati.cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   manage repositories
        
        Usage: cati repos [options]
        
        Options:
        -e|--edit: open repositories config file with editor
        -a|--add [new-repo]: add new repository
        --scan [directory]: scans packages inside in a directory and creates data files for repo
        -q|--quiet: quiet output
        
        Repo config structure:
        <url> pkg=<type(s) of packages. for example `cati` or `deb`> arch=<wanted architecture> channel=<wanted version channel(s)> name=<an name for repo> priority=<priority between another repos>
        
        Example:
        https://pkg.example.com/packages pkg=cati arch=all,i386 name=main-repo
        file:///path/to/packages pkg=cati,deb arch=all channel=alpha,security name=deb-repo

    `run(self)`
    :   Run command