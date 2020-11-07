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

    `state_item_to_string(state_item: dict) ‑> str`
    :   Gets an dictonary as a item in state list where returned by `BaseTransaction.state_list()`
        and generates an human readable message as string to show that message to user

    `state_list()`
    :   returns list of undoned transactions from state file