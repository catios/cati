Module frontend.RootRequired
============================
A tool to check program permission and if it haven't root permission, die the program

Functions
---------

    
`require_root_permission(is_cli=True, die_action=None)`
:   If `is_cli` argument is True, when user have not root permission,
    error will print in terminal. but if is False,
    the `die_action` will run as a function