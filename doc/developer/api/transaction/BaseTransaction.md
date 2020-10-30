Module transaction.BaseTransaction
==================================
Transaction base model.

transactions are install/remove/upgrade/downgrade operations.

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

    `pop_state()`
    :   remove first item from state