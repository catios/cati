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

    `has_any_thing(self)`
    :   returns is there any transactions to do

    `refresh_lists(self)`
    :   Refresh packages list and sync them with depends and conflicts

    `remove(self, pkgs: list)`
    :   Add packages to remove