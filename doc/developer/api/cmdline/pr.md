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

    
`exit(code=0)`
:   Exits program with exit code and deletes temp files before exit

    
`p(value='', end='\n')`
:   Prints on stdout