Module cati.cmdline.commands.PkgCommand
=======================================
Pkg command to work with .cati archives

Classes
-------

`PkgCommand()`
:   Pkg command to work with .cati archives

    ### Ancestors (in MRO)

    * cati.cmdline.BaseCommand.BaseCommand

    ### Methods

    `arch_error_event(self, pkg: cati.dotcati.ArchiveModel.BaseArchive)`
    :   installer arch_error event
        will run when package architecture is not supported on the system
        for example while installing `amd64` package on `i386` system

    `cannot_read_file_event(self, path)`
    :   index updater cannot_read_file event
        will pass to installer and installer passes this to index updater

    `config(self) ‑> dict`
    :   Define and config this command

    `dep_and_conflict_error_event(self, pkg: cati.dotcati.ArchiveModel.BaseArchive, ex: Exception)`
    :   installer dep_and_conflict_error event
        will run when package has conflict/dependency error while installing it
        `ex` argument can be DependencyError or ConflictError

    `directory_not_empty_event(self, package: cati.dotcati.ArchiveModel.BaseArchive, dirpath: str)`
    :   installer directory_not_empty event
        will run when package old directory is not empty

    `help(self)`
    :   work with .cati packages
        
        Usage: cati pkg [subcommand] [args] [options]
        
        Subcommands:
        - build:      build .cati package from directory(s)
        - show:       show content of .cati package(s). options: --files: show package files
        - install:    install a .cati package on system
        
        Options:
        - install subcommand:
        * --without-scripts: do not run package scripts in installation process
        * --target=[files-install-location-prefix-path]: set files installation prefix
        * --keep-conffiles: don't overwrite new version of config files
        * --force|-f: force install that packages are blocked in securiy blacklist

    `install_once(self, pkg: cati.dotcati.ArchiveModel.BaseArchive)`
    :   installs once package
        is called from install sub command

    `invalid_json_data_event(self, path, content)`
    :   index updater invalid_json_data event
        will pass to installer and installer passes this to index updater

    `package_currently_installed_event(self, package: cati.dotcati.ArchiveModel.BaseArchive, current_version: str)`
    :   installer package_currently_installed event
        will run when package already installed
        gets package and current installed version

    `package_installed_event(self, package: cati.dotcati.ArchiveModel.BaseArchive)`
    :   installer package_installed event
        will run when package installation finshed

    `package_new_installs_event(self, package: cati.dotcati.ArchiveModel.BaseArchive)`
    :   installer package_new_installs event
        will run when package will NEW installed

    `run(self)`
    :   Run command

    `show_once(self, pkg: cati.dotcati.ArchiveModel.BaseArchive)`
    :   shows once package (called from `show` subcommand function)
        gives package data to cli package sohwer component to show package info

    `start_run_any_script_event(self, package_name: str)`
    :   will run when starting running an `any` script

    `sub_build(self)`
    :   build subcommand (cati pkg build)

    `sub_install(self)`
    :   install sub command (cati pkg install)

    `sub_show(self)`
    :   show subcommand (cati pkg show)