#
# kernel.py
#
# the cati project
# Copyright 2020-2021 parsa shahmaleki <parsampsh@gmail.com>
#
# This file is part of cati.
#
# cati is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cati is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cati.  If not, see <https://www.gnu.org/licenses/>.
##################################################

""" Kernel of cli handler """

import sys
from . import ArgParser, pr
from .commands.HelpCommand import HelpCommand
from .commands.PkgCommand import PkgCommand
from .commands.ListCommand import ListCommand
from .commands.RemoveCommand import RemoveCommand
from .commands.ShowCommand import ShowCommand
from .commands.StateCommand import StateCommand
from .commands.QueryCommand import QueryCommand
from .commands.SearchCommand import SearchCommand
from .commands.FilesCommand import FilesCommand
from .commands.FinfoCommand import FinfoCommand
from .commands.RDependsCommand import RDependsCommand
from .commands.ForgetCommand import ForgetCommand
from .commands.CheckCommand import CheckCommand
from .commands.RepoCommand import RepoCommand
from .commands.UpdateCommand import UpdateCommand
from .commands.AutoremoveCommand import AutoremoveCommand
from .commands.ClearCacheCommand import ClearCacheCommand
from .commands.DownloadCommand import DownloadCommand
from .commands.InstallCommand import InstallCommand
from .commands.UpgradeCommand import UpgradeCommand
from .commands.FullUpgradeCommand import FullUpgradeCommand
from .commands.MeowCommand import MeowCommand

commands = {
    'help': HelpCommand,
    'pkg': PkgCommand,
    'list': ListCommand,
    'remove': RemoveCommand,
    'show': ShowCommand,
    'state': StateCommand,
    'query': QueryCommand,
    'search': SearchCommand,
    'files': FilesCommand,
    'finfo': FinfoCommand,
    'rdepends': RDependsCommand,
    'forget': ForgetCommand,
    'check': CheckCommand,
    'repo': RepoCommand,
    'update': UpdateCommand,
    'autoremove': AutoremoveCommand,
    'clear-cache': ClearCacheCommand,
    'download': DownloadCommand,
    'install': InstallCommand,
    'upgrade': UpgradeCommand,
    'full-upgrade': FullUpgradeCommand,
    'meow': MeowCommand,
}
"""
a dictonary from list of subcommands.
structure: "cmdname": CmdClass
"""

def handle(argv: list):
    """
    handle cli
    gets argv and runs entered command as subcommand (if not subcommand inserted, runs help command as default)

    Args:
        argv: the program arguments as list
    """
    # parse inserted arguments
    parsed_args = ArgParser.parse(argv)

    # find called subcommand by args
    if len(parsed_args['arguments']) == 0:
        # no subcommand called
        # call help command as default
        parsed_args['arguments'].append('help')

    try:
        command = commands[parsed_args['arguments'][0]]
    except:
        pr.e(sys.argv[0] + ': unknow command "' + parsed_args['arguments'][0] + '"')
        pr.exit(1)

    cmdobj = command()
    sys.exit(cmdobj.handle(parsed_args))
