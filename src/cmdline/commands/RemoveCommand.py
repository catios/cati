#
# RemoveCommand.py
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

''' Remove command '''

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi
from package.Pkg import Pkg
from transaction.Calculator import Calculator

class RemoveCommand(BaseCommand):
    def help(self):
        '''
        remove packages
        '''
        pass

    def define(self) -> dict:
        ''' Define and config this command '''
        return {
            'name': 'remove',
            'options': {
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def run(self):
        ''' Run command '''

        pr.p('Loading packages list...')
        print('=======================')
        # load list of packages
        packages = []
        for arg in self.arguments:
            pkg = Pkg.load_last(arg)
            if pkg == False:
                self.message('unknow package "' + arg + '"' + ansi.reset, before=ansi.red)
            else:
                packages.append(pkg)

        # start removing loaded packages
        calc = Calculator()
        calc.remove(packages)
        pr.p('Packages to remove:')
        for pkg in calc.to_remove:
            pr.p(pkg.data['name'])
