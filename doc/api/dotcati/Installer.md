Module dotcati.Installer
========================
Dotcati package installer

Functions
---------

    
`calc_file_sha256(filepath)`
:   gets filepath and calculates sha256 sum of that

Classes
-------

`Installer()`
:   Dotcati package installer

    ### Methods

    `check_dep_and_conf(self, pkg: dotcati.ArchiveModel.BaseArchive)`
    :   Checks package dependencies and conflicts.
        
        raises DependencyError when a dependency is not installed.
        
        raises ConflictError when a conflict is installed.

    `copy_files(self, pkg: dotcati.ArchiveModel.BaseArchive, directory_not_empty_event) ‑> list`
    :   Copy package files on system

    `copy_once_file(self, paths)`
    :   Copy one of package files

    `install(self, pkg: dotcati.ArchiveModel.BaseArchive, index_updater_events: dict, installer_events: dict, is_manual=True)`
    :   Install .cati package
        
        installer_events:
        - package_currently_install: gets the current installed version
        - package_new_installs: gets package archive
        - package_installed: will call after package installation
        - dep_and_conflict_error: will run when there is depends or conflict error
        - arch_error: will run when package arch is not sync with sys arch

    `load_files(self, path: str, base_temp_path: str)`
    :   Loads list of package files from extracted temp dir