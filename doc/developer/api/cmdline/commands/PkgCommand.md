Module cmdline.commands.PkgCommand
==================================
Pkg command to work with .cati archives

Classes
-------

`PkgCommand()`
:   Cmdline command model base

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `arch_error_event(self, pkg: dotcati.ArchiveModel.ArchiveModel)`
    :

    `cannot_read_file_event(self, path)`
    :

    `config(self) ‑> dict`
    :   Define and config this command

    `dep_and_conflict_error_event(self, pkg: dotcati.ArchiveModel.ArchiveModel, ex: Exception)`
    :

    `directory_not_empty_event(self, package: dotcati.ArchiveModel.ArchiveModel, dirpath: str)`
    :

    `help(self)`
    :   work with .cati packages
        Subcommands:
        - build:      build .cati package from directory(s)
        - show:       show content of .cati package(s). options: --files: show package files
        - install:    install a .cati package on system

    `install_once(self, pkg: dotcati.ArchiveModel.ArchiveModel)`
    :

    `invalid_json_data_event(self, path)`
    :

    `package_currently_installed_event(self, package: dotcati.ArchiveModel.ArchiveModel, current_version: str)`
    :

    `package_installed_event(self, package: dotcati.ArchiveModel.ArchiveModel)`
    :

    `package_new_installs_event(self, package: dotcati.ArchiveModel.ArchiveModel)`
    :

    `run(self)`
    :   Run command

    `show_once(self, pkg: dotcati.ArchiveModel.ArchiveModel)`
    :

    `sub_build(self)`
    :

    `sub_install(self)`
    :

    `sub_show(self)`
    :