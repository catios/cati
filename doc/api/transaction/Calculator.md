Module transaction.Calculator
=============================
Transaction calculator.

transaction calculator gets a list from packages for
install/remove/upgrade/downgrade operations
and calculates all of operations needed to be done
(actualy, includes dependencies, conflicts...)

Classes
-------

`Calculator()`
:   Transaction calculator

    ### Methods

    `get_sorted_list(self)`
    :   returns sorted list of all of packages

    `handle_install_conflicts(self)`
    :   Adds installable packages conflicts to install list

    `handle_install_depends(self)`
    :   Adds installable packages depends to install list

    `handle_install_reverse_conflicts(self)`
    :   Adds installable packages reverse conflicts to install list

    `handle_install_reverse_depends(self)`
    :   Adds installable packages reverse conflicts to install list

    `has_any_thing(self)`
    :   returns is there any transactions to do

    `install(self, pkgs: list)`
    :   Add packages for install

    `refresh_lists(self)`
    :   Refresh packages list and sync them with depends and conflicts

    `remove(self, pkgs: list)`
    :   Add packages to remove