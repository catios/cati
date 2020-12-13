Module cmdline.commands.RemoveCommand
=====================================
Remove command

Classes
-------

`RemoveCommand()`
:   Remove command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `dir_is_not_empty_event(self, pkg: package.Pkg.Pkg, f: str)`
    :   will run as package remover event when remover wants to remove a directory
        but that dir is not empty. this event shows a warning to user

    `help(self)`
    :   remove packages
        
        Usage: cati remove pkg1 pkg2 [options]
        
        Options:
        -y|--yes: do not ask for user confirmation
        --conffiles: also remove conffiles (full remove)
        --without-scripts: do not run package scripts in remove process
        --force|-f: force remove essential packages

    `package_remove_finished_event(self, pkg: package.Pkg.Pkg)`
    :   will run as package remover event when package remove process finished

    `removing_package_event(self, pkg: package.Pkg.Pkg)`
    :   will run as package remover event while starting removing a package

    `run(self)`
    :   Run command

    `start_run_any_script_event(self, package_name: str)`
    :   will run when starting running an `any` script