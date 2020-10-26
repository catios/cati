# State system
cati has a system named `state system`. this system created to keep packages transaction state.
for example, when we want to remove some packages, first we write this operations in state file, next doing that oprtations one by one. after doing one operation, we remove that from state list, and when all of operations done, state file will be empty.

now, if computer be shutdown while removing/installing some packages, in next boot, cati checks state and if state is not empty, means some operations need to be done and continues that transactions.
