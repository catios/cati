Module cmdline.kernel
=====================
Kernel of cli handler

Variables
---------

    
`commands`
:   a dictonary from list of subcommands.
    structure: "cmdname": CmdClass

Functions
---------

    
`handle(argv: list)`
:   handle cli
    gets argv and runs entered command as subcommand (if not subcommand inserted, runs help command as default)
    
    Args:
        argv: the program arguments as list