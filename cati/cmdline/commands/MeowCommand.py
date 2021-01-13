#
# MeowCommand.py
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

""" Meow command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr

class MeowCommand(BaseCommand):
    """ Meow command """
    def help(self):
        """
        Cati is a super cat, Meowwwww...!
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'meow',
            'options': {
            },
            'max_args_count': None,
            'min_args_count': None,
        }

    def run(self):
        """ Run command """
        pr.p("""
               /\       /\            * * * * * * * * * * * * * *
               | |_____| |            * Meow.....! I am Cati!   *
              |  --   --  |       ....* I can manage your       *
             |  { { * } }  | ..../    * Packages!               *
              |           |           *                         *
     __________|         |            * * * * * * * * * * * * * *
    /                     |
   /                      |
__/_  __  _________  _   _|
    |_| |_|       |_| |_|
""")
