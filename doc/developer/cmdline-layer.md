# Cmdline layer

the command line layer in cati is in `src/cmdline` folder.

### commands
cli commands are in `src/cmdline/commands` folder.

command template:

```python

''' Some command '''

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi

# commands should be a class and extends from BaseCommand
class SomeCommand(BaseCommand):
    def help(self):
        '''
        help of command as docstring
        '''
        pass

    def define(self) -> dict:
        ''' Define and config this command '''
        return {
            'name': 'somename', # name of the command
            'options': {
                # options should be a array
                # first item is for `is-required` property of command
                # second item is for `can-get-value` property of command
                # if first item is True, means this option is required
                # if second item is True, means a value should be assign to option
                '--first-option': [False, False], # [is-required, can-get-value]
                '-a': [False, False]
                '-another-option': [False, False]
            },

            # this option is for setting command max argument count
            'max_args_count': 1,

            # this option is for setting command min argument count
            # for example if command requires a argument, this option should be 1 or more
            'min_args_count': 0,
            # `None` value for above options means there is not max/min limitation
        }

    def run(self):
        ''' Run command '''
        # main function to run command
        pr.p('hello world')

```

### printing
we never use `print` function directly in commands. we use `pr` module insead of that:

```python
from cmdline import pr

# ...

pr.p('hello world') # print in stdin

pr.e('error') # print in stderr

pr.p('hello', end=' ') # use `end` argument

# ...

```
