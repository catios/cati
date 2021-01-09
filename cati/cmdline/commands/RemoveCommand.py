#
# RemoveCommand.py
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

""" Remove command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.cmdline.components import TransactionShower, StateContentShower
from cati.dotcati.Pkg import Pkg
from cati.transaction.Calculator import Calculator
from cati.transaction.Remove import Remove
from cati.transaction.BaseTransaction import BaseTransaction
from cati.frontend.RootRequired import require_root_permission

class RemoveCommand(BaseCommand):
    """ Remove command """
    def help(self):
        """
        remove packages

        Usage: cati remove pkg1 pkg2 [options]

        Options:
        -y|--yes: do not ask for user confirmation
        --conffiles: also remove conffiles (full remove)
        --without-scripts: do not run package scripts in remove process
        --force|-f: force remove essential packages
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'remove',
            'options': {
                '-y': [False, False],
                '--yes': [False, False],
                '--conffiles': [False, False],
                '--without-scripts': [False, False],
                '--force': [False, False],
                '-f': [False, False],
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def removing_package_event(self, pkg: Pkg):
        """
        will run as package remover event while starting removing a package
        """
        pr.p(
            'Removing ' + ansi.yellow + pkg.data['name'] + ' (' + pkg.data['version'] + ')' + ansi.reset + '...',
            end=' '
        )

    def package_remove_finished_event(self, pkg: Pkg):
        """
        will run as package remover event when package remove process finished
        """
        pr.p(ansi.green + 'OK' + ansi.reset)

    def dir_is_not_empty_event(self, pkg: Pkg, f: str):
        """
        will run as package remover event when remover wants to remove a directory
        but that dir is not empty. this event shows a warning to user
        """
        self.message('warning: directory "' + f.split(':', 1)[1] + '" is not emptry and will not be delete' + ansi.yellow, before=ansi.reset)

    def start_run_any_script_event(self, package_name: str):
        """ will run when starting running an `any` script """
        pr.p('Processing scripts for ' + package_name + '...')

    def run(self):
        """ Run command """

        require_root_permission()

        # check transactions state before run new transactions
        pr.p('Checking transactions state...')
        state_list = BaseTransaction.state_list() # get list of undoned transactions
        if state_list:
            # the list is not empty
            StateContentShower.show(state_list)
            return 1

        pr.p('Loading packages list...')
        pr.p('==============================')
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

        essential_packages = []
        for pkg in calc.to_remove:
            try:
                if pkg.data['essential']:
                    essential_packages.append(pkg)
            except:
                pass

        if not self.has_option('--force') and not self.has_option('-f'):
            for pkg in essential_packages:
                pr.p(ansi.red + 'Package "' + pkg.data['name'] + '" is a essential package and cannot be remove. use --force|-f option to force remove them' + ansi.reset)
            if essential_packages:
                return 1

        if not calc.has_any_thing():
            return

        # check user confirmation
        if not self.has_option('-y') and not self.has_option('--yes'):
            pr.p('Do you want to continue? [Y/n] ', end='')
            answer = input()
            if not (answer == 'y' or answer == 'Y' or answer == ''):
                pr.p(ansi.yellow + 'Abort.' + ansi.reset)
                pr.exit(1)

        # add packages to state
        BaseTransaction.add_to_state(calc)

        packages_to_remove_names_and_versions = [pkg.data['name'] + '@' + pkg.data['version'] for pkg in calc.to_remove]

        # run transactions
        for pkg in calc.to_remove:
            Remove.run(
                pkg,
                {
                    'removing_package': self.removing_package_event,
                    'package_remove_finished': self.package_remove_finished_event,
                    'dir_is_not_empty': self.dir_is_not_empty_event,
                },
                self.has_option('--conffiles'),
                run_scripts=(not self.has_option('--without-scripts'))
            )
            BaseTransaction.pop_state()

        BaseTransaction.run_any_scripts(['remove', packages_to_remove_names_and_versions], events={
            'start_run_script': self.start_run_any_script_event,
        })

        BaseTransaction.finish_all_state()
