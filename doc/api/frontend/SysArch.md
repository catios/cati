Module frontend.SysArch
=======================
Handle system architecture

Variables
---------

    
`is_testing`
:   in testing environment,
    default architecture is `i386`, not real host arch.

Functions
---------

    
`allowed_archs() ‑> list`
:   Returns list of allowed architectures to install on the system
    
    The default archs are `all` and system architecture. also more archs
    will be loaded from /etc/cati/allowed-architectures.list
    
    Returns:
        list: list of allowed archs like ['all', 'amd64', '...']

    
`sys_arch() ‑> str`
:   Returns system architecture