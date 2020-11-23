#
# AutoremoveCommand.py
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

""" Autoremove command """

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi, ArgParser
from package.Pkg import Pkg
from cmdline.commands.RemoveCommand import RemoveCommand

class AutoremoveCommand(BaseCommand):
    """ Autoremove command """
    def help(self):
        """
        remove unused automaticaly installed packages

        Usage: cati autoremove [options]

        Options:
        -y|--yes: do not ask for user confirmation
        --conffiles: also remove conffiles (full remove)
        --without-scripts: do not run package scripts in remove process
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'autoremove',
            'options': {
                '-y': [False, False],
                '--yes': [False, False],
                '--conffiles': [False, False],
                '--without-scripts': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def find_unused_packages(self):
        """ finds unused packages """
        all_packages = Pkg.all_list()['list']

        for pkg in all_packages:
            try:
                if Pkg.is_installed(pkg.data['name']):
                    if not Pkg.is_installed_manual(pkg.data['name']):
                        has_any_reverse_depends = False
                        reverse_depends = Pkg.load_version(pkg.data['name'], Pkg.installed_version(pkg.data['name'])).get_reverse_depends()
                        for rdep in reverse_depends:
                            if rdep.installed():
                                rdep_is_in_unused_packages = False
                                for upkg in self.unused_packages:
                                    if upkg.data['name'] == rdep.data['name']:
                                        rdep_is_in_unused_packages = True
                                if not rdep_is_in_unused_packages:
                                    has_any_reverse_depends = True
                        if not has_any_reverse_depends:
                            self.unused_packages.append(pkg)
            except:
                pass

    def run(self):
        """ Run command """

        if not self.is_quiet():
            pr.p('Checking unused packages...')

        self.unused_packages = []
        self.find_unused_packages()
        unused_packages = self.unused_packages

        package_names = [pkg.data['name'] for pkg in unused_packages]
        options = [op for op in self.args['options']]

        if not package_names:
            pr.p('There is not any unused package')
            return 0

        remove_cmd = RemoveCommand()
        return remove_cmd.handle(ArgParser.parse(['cati', 'remove', *package_names, *options]))
