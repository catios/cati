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
from cmdline.components import TransactionShower
from package.Pkg import Pkg
from transaction.Calculator import Calculator
from transaction.runners.Remove import Remove
from transaction.BaseTransaction import BaseTransaction
from frontend.RootRequired import require_root_permission

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
                '-y': [False, False],
                '--yes': [False, False],
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def removing_package_event(self, pkg: Pkg):
        pr.p(
            'Removing ' + ansi.yellow + pkg.data['name'] + ' (' + pkg.data['version'] + ')' + ansi.reset + '...',
            end=' '
        )

    def package_remove_finished_event(self, pkg: Pkg):
        pr.p(ansi.green + 'OK' + ansi.reset)

    def dir_is_not_empty_event(self, pkg: Pkg, f: str):
        self.message('warning: directory "' + f.split(':', 1)[1] + '" is not emptry and will not be delete' + ansi.yellow, before=ansi.reset)

    def run(self):
        ''' Run command '''

        require_root_permission()

        pr.p('Loading packages list...')
        pr.p('=======================')
        # load list of packages
        packages = []
        for arg in self.arguments:
            pkg = Pkg.load_last(arg)
            if pkg == False:
                self.message('unknow package "' + arg + '"' + ansi.reset, before=ansi.red)
            else:
                if pkg.installed():
                    packages.append(pkg)
                else:
                    self.message('package "' + pkg.data['name'] + '" is not installed' + ansi.reset, before=ansi.red)

        # start removing loaded packages
        calc = Calculator()
        calc.remove(packages)

        # show transactions
        TransactionShower.show(calc)

        if not calc.has_any_thing():
            return

        # check user confirmation
        if not self.has_option('-y') and not self.has_option('--yes'):
            pr.p('Do you want to continue? [Y/n] ', end='')
            answer = input()
            if not (answer == 'y' or answer == 'Y' or answer == ''):
                pr.p(ansi.yellow + 'Abort.' + ansi.reset)
                pr.exit(1)

        # run transactions
        for pkg in calc.to_remove:
            Remove.run(
                pkg,
                {
                    'removing_package': self.removing_package_event,
                    'package_remove_finished': self.package_remove_finished_event,
                    'dir_is_not_emptry': self.dir_is_not_empty_event,
                }
            )

        BaseTransaction.finish_all_state()
