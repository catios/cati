Module cmdline.pr
=================
Print handling in cli

Variables
---------

    
`is_testing`
:   if this variable is True, print will be disable. this variable will get True value while running tests to hide prints

Functions
---------

    
`e(value='', end='\n')`
:   Prints on stderr
    
    Args:
        value: that value you want to print
        end: the end of line (default is `\n`)

    
`exit(code=0)`
:   Exits program with exit code and deletes temp files before exit
    
    Args:
        code: the exit code (default 0)

    
`p(value='', end='\n')`
:   Prints on stdout
    
    Args:
        value: that value you want to print
        end: the end of line (default is `\n`)