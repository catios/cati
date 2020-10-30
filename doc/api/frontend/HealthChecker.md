Module frontend.HealthChecker
=============================
Checks cati installation health and repair

Functions
---------

    
`check(events: dict)`
:   Check all of needed files and dirs for cati installation
    
    events:
    - failed_to_repair: will run when cati installation is corrupt and user has not root permission
    to repair it and passes filepath and type of that to function

    
`repair_once_dir(dirpath: str, events: dict)`
:   Repairs once dir

    
`repair_once_file(filepath: str, events: dict)`
:   Repairs once file