Module cati.cmdline.commands.DownloadCommand
============================================
Download command

Classes
-------

`DownloadCommand()`
:   Download command

    ### Ancestors (in MRO)

    * cati.cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `download_once(self, pkg, output=None)`
    :   Download once package

    `help(self)`
    :   download packages
        
        Usage: cati download pkg1 pkg1 ... [options]
        ...... cati download pkg=<version> pkg2=<version> pkg3 ... [options]
        ...... cati download pkg=<version>=<arch> ... [options]
        
        Options:
        --output=[output file path]: set file download path
        -q|--quiet: quiet output

    `run(self)`
    :   Run command