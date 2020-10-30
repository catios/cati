Module cmdline.commands.ListCommand
===================================
List command

Classes
-------

`ListCommand()`
:   Cmdline command model base

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   shows list of packages
        Options:
        --installed: show only installed packages
        --installed-manual: show only manual installed packages
        -q|--quiet: quiet output, only show package names

    `run(self)`
    :   Run command

    `show_once(self, package: package.Pkg.Pkg)`
    :