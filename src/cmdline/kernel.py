#
# kernel.py
#
# the cati project
# Copyright 2020 parsa mpsh <parsampsh@gmail.com>
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
from cmdline import ArgParser, pr
from cmdline.commands.HelpCommand import HelpCommand
from cmdline.commands.PkgCommand import PkgCommand
from cmdline.commands.ListCommand import ListCommand
from cmdline.commands.RemoveCommand import RemoveCommand
from cmdline.commands.ShowCommand import ShowCommand
from cmdline.commands.StateCommand import StateCommand
from cmdline.commands.QueryCommand import QueryCommand
from cmdline.commands.SearchCommand import SearchCommand
from cmdline.commands.FilesCommand import FilesCommand
from cmdline.commands.FinfoCommand import FinfoCommand
from cmdline.commands.RDependsCommand import RDependsCommand

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
}
"""
a dictonary from list of subcommands
structure: "cmdname": CmdClass
"""

def handle(argv: list):
    """
    handle cli
    gets argv and runs entered command as subcommand (if not subcommand inserted, runs help command as default)
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
