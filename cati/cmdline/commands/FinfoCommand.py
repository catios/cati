#
# FinfoCommand.py
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

""" Finfo command """

import os
from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi

class FinfoCommand(BaseCommand):
    """ Finfo command """
    def help(self):
        """
        shows info about an file

        this command says an file is for which package and some another details

        Usage: cati finfo /path/to/file
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'finfo',
            'options': {
            },
            'max_args_count': 1,
            'min_args_count': 1,
        }

    def run(self):
        """ Run command """

        if not os.path.exists(self.arguments[0]):
            pr.e('file "' + self.arguments[0] + '" not exists.')
            return 1

        filepath = os.path.abspath(self.arguments[0])

        return os.system(self.cati_exec + ' files --installed | grep ": ' + filepath + '"')
