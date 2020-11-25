Module cmdline.commands.FullUpgradeCommand
==========================================
FullUpgrade command

Classes
-------

`FullUpgradeCommand()`
:   FullUpgrade command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   update, upgrade and autoremove
        
        Usage: cati full-upgrade [options]
        
        Options:
        -y|--yes: don't ask for user confirmation

    `run(self)`
    :   Run command