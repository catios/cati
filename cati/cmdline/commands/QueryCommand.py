#
# QueryCommand.py
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

""" Query command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.dotcati.Pkg import Pkg

class QueryCommand(BaseCommand):
    """ Query command """
    def help(self):
        """
        checks a package query

        Usage: cati query [query]
        ...... cati query "somepackage >= 1.0"
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'query',
            'options': {
                '-q': [False, False],
                '--quiet': [False, False],
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

        result = Pkg.check_state(full_query_string)

        if result:
            if not self.is_quiet():
                pr.p(ansi.green + 'True' + ansi.reset)
            return 0
        else:
            if not self.is_quiet():
                pr.p(ansi.red + 'False' + ansi.reset)
            return 1
