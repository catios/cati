Module cati.dotcati.Installer
=============================
Dotcati package installer

Classes
-------

`Installer()`
:   Dotcati package installer

    ### Methods

    `add_package_to_lists(self, pkg: cati.package.Pkg.Pkg, index_updater_events: dict)`
    :   Adds the package information to database
        
        Args:
            pkg (Pkg): the package
            index_updater_events (dict): events for index updater

    `check_dep_and_conf(self, pkg: cati.dotcati.ArchiveModel.BaseArchive)`
    :   Checks package dependencies and conflicts.
        
        Args:
            pkg: (BaseArchive) the package archive object
        
        Raises:
            DependencyError: when a dependency is not installed (dependency will put in exception message)
            ConflictError: when a conflict is installed (conflict will put in exception message)

    `check_security_blacklist(self, pkg: cati.dotcati.ArchiveModel.BaseArchive)`
    :   checks package sha256, sha512 and md5 and checks this hashes in security blacklist.
        
        Args:
            pkg (BaseArchive): the package archive object
        
        Raises:
            dotcati.exceptions.PackageIsInSecurityBlacklist: when package is blocked in security blacklist
                (the blacklist details will put in `blacklist_item` attribute of exception object)

    `copy_files(self, pkg: cati.dotcati.ArchiveModel.BaseArchive, directory_not_empty_event, target_path='') ‑> list`
    :   Copy package files on system
        
        Args:
            pkg (BaseArchive): the package archive object
            directory_not_empty_event (callable): the function will be run when we want to delete old direcotry
                                      of package and that is not empty.
            target_path (str): target path prefix of copied files location. default is `/` means
                               copies files on the root directory. you can change it.
        
        Returns:
            list[str]: list of copied files

    `copy_once_file(self, paths)`
    :   Copy one of package files (this method is called from `copy_files` method)

    `install(self, pkg: cati.dotcati.ArchiveModel.BaseArchive, index_updater_events: dict, installer_events: dict, is_manual=True, run_scripts=True, target_path='', keep_conffiles=False, check_security_blacklist=True)`
    :   Install .cati package
        
        Args:
            pkg (BaseArchive): the package archive object
            index_updater_events (dict): events will be passed to `dotcati.ListUpdater.update_indexes()`
            installer_events (dict): The events
                - package_currently_install: gets the current installed version
                - package_new_installs: gets package archive
                - package_installed: will call after package installation
                - dep_and_conflict_error: will run when there is depends or conflict error
                - arch_error: will run when package arch is not sync with sys arch
            is_manual (bool): installed package as manual or not (default is True means manual)
            run_scripts (bool): run package install scripts or not (default is True)
            target_path (str): where is the target path for installed files (will pass to `self.copy_files()`)
            keep_conffiles (bool): stil keep config files if changed (default is True)
            check_security_blacklist (bool): check package is in security blacklist or not

    `load_files(self, path: str, base_temp_path: str)`
    :   Loads list of package files from extracted temp dir
        
        you should set `self.loaded_files` list before call this.
        this method will put loaded files in self.loaded_files list
        
        Args:
            path (str): that directory you want to load files list from that
            base_temp_path (str): base path of package extracted temp directory

    `run_script(self, script_name: str, script_path=None)`
    :   runs an script in the package (only install scripts)
        
        Args:
            script_name (str): name of that script you want to run
            script_path (str, None): you can change the default path of script file with this argument
        
        Raises:
            dotcati.exceptions.PackageScriptError: when script returns non-zero exit code
                (exit code will put in `error_code` attribute of exception object)