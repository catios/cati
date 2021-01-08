Module cati.frontend.Env
========================
Handle environment file paths.

in cati, we do not write config, database and... file paths directly in everywhere.
we get that paths from this module.
also testing system changes base environment path in `base_path_dir` variable
to isolate program environemnt while running tests

Variables
---------

    
`base_path_dir`
:   str: base path of the cati files environment.
    (will get another path in testing environment to isolate testing environment with real environment)

Functions
---------

    
`allowed_archs()`
:   

    
`any_scripts(path='')`
:   Any scripts directory

    
`base_path(path='')`
:   Returns environment base path

    
`cache_dir(path='')`
:   

    
`installed_lists(path='')`
:   Installed packages list directory

    
`packages_lists(path='')`
:   Packages list directory

    
`repos_config()`
:   

    
`repos_config_dir(path='')`
:   

    
`security_blacklist(path='')`
:   Security blacklist directory

    
`state_file()`
:   State file (read state system documentation)

    
`unremoved_conffiles()`
:   Unremoved conffiles list filepath