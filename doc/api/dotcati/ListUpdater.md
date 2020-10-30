Module dotcati.ListUpdater
==========================
Packages list updater

Functions
---------

    
`update_indexes(events: dict)`
:   This function loads available versions of a package and index them in index file
    and do this action for all of packages in lists.
    
    the `events` argument should be a dictonary from functions. this will use to handle errors
    for example if some thing went wrong, the spesific function in events
    will run.
    
    events:
    - cannot_read_file: if in this process, an error happened while reading a file, this will run with file path arg
    - invalid_json_data: if json content of a file is curropt, this will run with file path and content args