Module cmdline.BaseCommand
==========================
Cmdline command model base

Classes
-------

`BaseCommand()`
:   Cmdline command model base

    ### Descendants

    * cmdline.commands.AutoremoveCommand.AutoremoveCommand
    * cmdline.commands.CheckCommand.CheckCommand
    * cmdline.commands.ClearCacheCommand.ClearCacheCommand
    * cmdline.commands.DownloadCommand.DownloadCommand
    * cmdline.commands.FilesCommand.FilesCommand
    * cmdline.commands.FinfoCommand.FinfoCommand
    * cmdline.commands.ForgetCommand.ForgetCommand
    * cmdline.commands.FullUpgradeCommand.FullUpgradeCommand
    * cmdline.commands.HelpCommand.HelpCommand
    * cmdline.commands.InstallCommand.InstallCommand
    * cmdline.commands.ListCommand.ListCommand
    * cmdline.commands.PkgCommand.PkgCommand
    * cmdline.commands.QueryCommand.QueryCommand
    * cmdline.commands.RDependsCommand.RDependsCommand
    * cmdline.commands.RemoveCommand.RemoveCommand
    * cmdline.commands.RepoCommand.RepoCommand
    * cmdline.commands.SearchCommand.SearchCommand
    * cmdline.commands.ShowCommand.ShowCommand
    * cmdline.commands.StateCommand.StateCommand
    * cmdline.commands.UpdateCommand.UpdateCommand
    * cmdline.commands.UpgradeCommand.UpgradeCommand

    ### Methods

    `general_help(self)`
    :   returns general help of cati cli

    `handle(self, args: dict)`
    :   Handle run the command
        first, validates arguments
        next, checks if --help inserted, show command help
        if not, run command

    `has_option(self, option: str)`
    :   Checks the option is inserted

    `help_full(self, with_general_help=True)`
    :   Returns full help of command
        the `with_general_help` argument used to include/exclude general help of cati

    `help_summary(self)`
    :   Returns summary of help (first line only)

    `is_quiet(self)`
    :   Checks --quiet and -q options

    `is_verbose(self)`
    :   Checks --verbose and -v options

    `message(self, msg, is_error=False, before='')`
    :   Prints a message like this:
        cati: <command-name>: <the-message>
        
        arguments:
        - `is_error`: if this is True, message will print on stderr
        - `before`: before will print in the first of message

    `option_value(self, option: str)`
    :   Returns value of option

    `validate(self, args: dict)`
    :   Validate inserted arguments in command config frame
        loads command config from `config` function output
        next checks arguments and compares them with command config
        then, if an unknow option is inserted or more/less argument inserted,
        shows error to user