#
# HelpCommand.py
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

''' Help command '''

from cmdline.BaseCommand import BaseCommand
from cmdline import pr

class HelpCommand(BaseCommand):
    def help(self):
        '''
        Help of command
        '''
        pass

    def define(self) -> dict:
        ''' Define and config this command '''
        return {
            'name': 'help',
            'options': {
                '-v': [False , False], # [is-required , can-get-value]
                '--version': [False , False]
            },
            'max_args_count': 1,
            'min_args_count': 0,
        }

    def run(self):
        ''' Run command '''
        self.message('Hello world!')
