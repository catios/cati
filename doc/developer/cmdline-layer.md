# Cmdline layer

the command line layer in cati is in `cati/cmdline` folder.

### commands
cli commands are in `cati/cmdline/commands` folder.

command template:

```python

""" Some command """

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi

# commands should be a class and extends from BaseCommand
class SomeCommand(BaseCommand):
    def help(self):
        """
        help of command as docstring
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
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
        """ Run command """
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

### listing commands

if you create a command in `cati/cmdline/commands`, that command will not include in program.
you should add created command to list of commands

to do this, you should open `cati/cmdline/kernel.py`.
next, import your command in that:

```python
# ...

from cmdline.commands.YourCommand import YourCommand

# ...
```

next, add imported class to `commands` list:

```python
# ...

# subcommands list
commands = {
    # ...
    'thecmd': YourCommand,
    # ...
}

# ...
```

now your command is included in cmdline layer.

### BaseCommand functions

there is some helper functions in command classes.

for example:
```python


""" Some command """

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi

# commands should be a class and extends from BaseCommand
class SomeCommand(BaseCommand):
    def help(self):
        """
        help of command as docstring
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
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
        """ Run command """
        # example for `message` helper function
        self.message('hello world') # output: cati: somecmd: hello world

        # `before` argument
        self.message('hello world', before='hi ') # output: hi cati: somecmd: hello world

        # `is_error` argument
        self.message('hello world', is_error=True) # this will print in stderr (default is False)


```

#### another helper functions

- `has_option('--some-option') -> Boolean` | checks an option is inserted or not
- `option_value('--some-option') -> string` | returns assigned value to a option. for example: `cati somecommand --some-option='some value'`
- `help_summary() -> string` | returns command help summary (first line of help docstring is `help` function)
- `help_full(with_general_help=True) -> string` | returns full help of command. if `with_general_help` argument be True, general help for cati commands will include in output but if be False, just help of command will return

### Ansi

to print colored texts, you can use `cmdline.ansi` module.

for example:

```python
# ...

from cmdline import ansi

pr.p(ansi.green + 'hello' + ansi.reset) # output is an green `hello`

# ...
```

you have to write your text after `ansi.<somecolor>`, and next to finish colored text write `ansi.reset`.

#### another ansi items

- `ansi.header`
- `ansi.blue`
- `ansi.green`
- `ansi.yellow`
- `ansi.red`
- `ansi.bold`
- `ansi.underline`

also there is a `ansi.disable()` function. this function disable all of ansi items (means all of program output will not has any ansi).
