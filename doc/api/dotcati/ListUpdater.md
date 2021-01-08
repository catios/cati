Module dotcati.ListUpdater
==========================
Database Packages list updater

Functions
---------

    
`index_reverse_depends_and_conflicts(pkg: cati.package.Pkg.Pkg)`
:   Packages have `depends` and `conflicts`
    But also they have `Reverse` depends and conflicts
    Reverse d/c should be indexed because loading them real time is so big process
    We index them in a place, and when a package is added/changed, this function should be called
    
    Args:
        pkg (Pkg): changed/added package (reverse c/d will be set for that packages this package is related to them)

    
`update_indexes(events: dict)`
:   This function loads available versions of a package and index them in index file
    and do this action for all of packages in lists.
    
    Args:
        events: (dict) the `events` argument should be a dictonary from functions. this will use to handle errors
                for example if some thing went wrong, the spesific function in events
                will run.
                events:
                - cannot_read_file: if in this process, an error happened while reading a file, this will run with file path arg
                - invalid_json_data: if json content of a file is curropt, this will run with file path and content args