Module cmdline.commands.InstallCommand
======================================
Install command

Classes
-------

`InstallCommand()`
:   Install command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   install packages
        
        Usage: cati install [options] pkg1 pkg2 pkg3 ...
        ...... cati install [options] pkg1 pkg2=<version> ...
        
        Options:
        -y|--yes: don't ask for user confirmation
        --reinstall: reinstall gived packages
        --download-only: only download packages. this helps you to only download packages and install them later
        --with-recommends: also install recommended packages
        --keep-conffiles: `pkg install --keep-conffiles`
        --without-scripts: `remove/install --without-scripts`
        --target=[target-installation-path]: `pkg install --target`

    `run(self)`
    :   Run command

    `set_manual_installs(self, packages)`
    :   Sets installed packages type (manual/auto)