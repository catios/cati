#
# ListCommand.py
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

""" List command """

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi
from package.Pkg import Pkg

class ListCommand(BaseCommand):
    def help(self):
        """
        shows list of packages
        Options:
        --installed: show only installed packages
        --installed-manual: show only manual installed packages
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'list',
            'options': {
                '--installed': [False, False],
                '--installed-manual': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def show_once(self, package: Pkg):
        output = ansi.green + package.data['name'] + ansi.reset + '/' +  ansi.yellow + package.data['version'] + ansi.reset
        if package.installed():
            if package.is_installed_manual(package.data['name']):
                output += '/Installed-Manual:' + ansi.blue + package.installed() + ansi.reset
            else:
                output += '/Installed:' + ansi.blue + package.installed() + ansi.reset
        output += '/[' + package.data['repo'] + ']'

        pr.p(output)

    def run(self):
        """ Run command """

        pr.p('Loading packages list...')
        pr.p('========================')
        # load list of packages
        if self.has_option('--installed'):
            # just list installed packages
            packages = Pkg.installed_list()
        elif self.has_option('--installed-manual'):
            packages = Pkg.installed_list()
            packages_list = [tmp_pkg for tmp_pkg in packages['list'] if Pkg.is_installed_manual(tmp_pkg.data['name'])]
            packages['list'] = packages_list
        else:
            packages = Pkg.all_list()

        for error in packages['errors']:
            self.message(error + ansi.reset, True, before=ansi.red)

        for package in packages['list']:
            self.show_once(package)
