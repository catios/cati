#
# SearchCommand.py
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

""" Search command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi, ArgParser
from .ListCommand import ListCommand

class SearchCommand(BaseCommand):
    """ Search command """
    def help(self):
        """
        search between packages by name and description

        (this command is a alias for `cati list --search='word'`)

        Usage: cati search 'word'
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'search',
            'options': {
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def run(self):
        """ Run command """

        # join all of arguments as one argument
        full_query_string = ''
        if len(self.arguments) > 1:
            for arg in self.arguments:
                full_query_string += arg + ' '
            full_query_string = full_query_string[:len(full_query_string)-1]
        else:
            full_query_string = self.arguments[0]

        # search arguments with `list --search` command
        arguments = ['--search=' + full_query_string]
        arguments.insert(0, 'cati')
        arguments.insert(1, 'list')
        list_command = ListCommand()
        return list_command.handle(ArgParser.parse(arguments))
