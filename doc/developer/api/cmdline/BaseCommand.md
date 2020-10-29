Module cmdline.BaseCommand
==========================
Cmdline command model base

Classes
-------

`BaseCommand()`
:   Cmdline command model base

    ### Descendants

    * cmdline.commands.HelpCommand.HelpCommand
    * cmdline.commands.ListCommand.ListCommand
    * cmdline.commands.PkgCommand.PkgCommand
    * cmdline.commands.RemoveCommand.RemoveCommand
    * cmdline.commands.ShowCommand.ShowCommand

    ### Methods

    `general_help(self)`
    :

    `handle(self, args: dict)`
    :   Handle run the command

    `has_option(self, option: str)`
    :   Checks the option is inserted

    `help_full(self, with_general_help=True)`
    :   Returns full help of command
        the `with_general_help` argument used to include/exclude general help of cati

    `help_summary(self)`
    :   Returns summary of help (first line only)

    `message(self, msg, is_error=False, before='')`
    :   Prints a message on screen

    `option_value(self, option: str)`
    :   Returns value of option

    `validate(self, args: dict)`
    :   Validate inserted arguments in command config frame