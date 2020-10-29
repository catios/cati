Module transaction.BaseTransaction
==================================
Transaction base model

Classes
-------

`BaseTransaction()`
:   Transaction base model

    ### Descendants

    * transaction.runners.Remove.Remove

    ### Static methods

    `add_to_state(calc: transaction.Calculator.Calculator)`
    :   add new item to state

    `finish_all_state()`
    :   clear all of states

    `finish_last_state()`
    :   set last item in state to finished

    `handle_state(section: str, pkg: package.Pkg.Pkg)`
    :   add new item to state

    `pop_state()`
    :   add new item to state