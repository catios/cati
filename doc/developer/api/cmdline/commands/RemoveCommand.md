Module cmdline.commands.RemoveCommand
=====================================
Remove command

Classes
-------

`RemoveCommand()`
:   Cmdline command model base

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `dir_is_not_empty_event(self, pkg: package.Pkg.Pkg, f: str)`
    :

    `help(self)`
    :   remove packages

    `package_remove_finished_event(self, pkg: package.Pkg.Pkg)`
    :

    `removing_package_event(self, pkg: package.Pkg.Pkg)`
    :

    `run(self)`
    :   Run command