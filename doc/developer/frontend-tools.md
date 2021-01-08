# Frontend tools
there is some tools in `cati/frontend` folder.
this tools are releated to host

## Env
this module contains some functions to handle file paths.
this is created to we use this to get some specify paths and do not write that paths everywhere.

```python
# ...

from frontend import Env

Env.base_path() # base path of environment (default is '/')

Env.packages_lists() # directory of packages list database

Env.installed_lists() # directory of installed packages list database

Env.state_file() # path of state file

# ...
```

related:
- [(files and dirs structure)](/doc/files-and-dirs-structure.md)
- [(State system)](/doc/developer/state-system.md)

## HealthChecker
this module checks cati installation health

```python
# ...

from frontend import HealthChecker

# checks all of cati files and directories and if there is some problems, repair them
HealthChecker.check({})

# ...
```

`HealthChecker.check()` function gets a dictonary as argument. this argument named `events`.
this dictonary should has `failed_to_repair` item. this item should be a function.

look at this example:

```python
# ...

from cmdline import pr
from frontend import HealthChecker

def failed_to_repair():
    # this function will run when cati installation is corrupt
    # and user has not root access to repair it
    pr.p('cati installation is corrupt. we do not have root access to repair it')

HealthChecker.check({
    'failed_to_repair': failed_to_repair
})

# ...
```

related:
- [(Event pettern)](/doc/developer/event-pattern.md)

## RootRequired
this module has a function to check root access

```python
# ...

from frontend.RootRequired import require_root_permission

# when you run this function, this tool checks root access
# if user has not root access, program will show an cli error and exits
require_root_permission()

# ...
```

also this function has two optional arguments: `is_cli`, `die_action`.

if you want to handle error without command line error, you can put `False` in `is_cli` and pass a function in `die_action`:

```python
def user_has_not_root_permission():
    # do something when user has not root permission
    pass

require_root_permission(is_cli=False, die_action=user_has_not_root_permission)
```

## SysArch
this module has a function to return system architecture:

```python
# ...

from frontend import SysArch

arch = SysArch.sys_arch() # returns system architecture

# ...
```

## Temp
this module is for handling temp files:

```python
# ...

from frontend import Temp

# creates a temp directory and returns path of that
Temp.make_dir()

# creates a temp file and returns path of that
Temp.make_file()

# deletes all of created temp files
Temp.clean()

# ...
```

## Version
the `cati/frontend/Version.py` file keeps cati installation version in `version` variable.
