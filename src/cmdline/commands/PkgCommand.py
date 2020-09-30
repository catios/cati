#
# PkgCommand.py
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


''' Pkg command to work with .cati archives '''

from cmdline.BaseCommand import BaseCommand
from cmdline import pr

class PkgCommand(BaseCommand):
    def help(self):
        '''
        work with .cati packages
        
        Subcommands:
        -   build:      build .cati package from directory(s)
        -   show:       show content of .cati package(s)
        -   install:    install a .cati package on system
        '''
        pass

    def define(self) -> dict:
        ''' Define and config this command '''
        return {
            'name': 'help',
            'options': {
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def sub_build(self):
        pr.p('Pkg Build')

    def sub_show(self):
        pr.p('Pkg Show')

    def sub_install(self):
        pr.p('Pkg Install')

    def run(self):
        ''' Run command '''
        if self.args['arguments'][0] == 'build':
            return self.sub_build()
        elif self.args['arguments'][0] == 'show':
            return self.sub_show()
        elif self.args['arguments'][0] == 'install':
            return self.sub_install()
        else:
            self.message('unknow subcommand "' + self.args['arguments'][0] + '"' , True)
            return 1
