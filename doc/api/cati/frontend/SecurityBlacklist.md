Module cati.frontend.SecurityBlacklist
======================================
Cati has a feature to block malware packages (detected)
this feature is a database from sha256, md5 and sha512 hashes
this database declares the malware packages.
cati checks packages hashes and checks them in this database.
if package is in database, will not install and user will get error
"this package is a malware" and details of database

Functions
---------

    
`get_list() ‑> list`
:   returns list of blaclist items
    
    Returns:
        list: returns list of blacklist items