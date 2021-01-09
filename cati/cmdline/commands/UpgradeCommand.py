#
# UpgradeCommand.py
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

""" Upgrade command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi, ArgParser
from cati.dotcati.Pkg import Pkg
from .InstallCommand import InstallCommand

class UpgradeCommand(BaseCommand):
    """ Upgrade command """
    def help(self):
        """
        upgrade all of packages

        Usage: sudo cati upgrade [options]

        Options: all of `install` command options
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        install_cmd_options = InstallCommand().config()['options']
        return {
            'name': 'upgrade',
            'options': install_cmd_options,
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """

        pr.p('Checking upgradable packages...')
        installed_packages = Pkg.installed_list()['list']
        upgradable_packages = []
        for pkg in installed_packages:
            installed_version = pkg.installed()
            latest_version = pkg.data['version']
            if Pkg.compare_version(latest_version, installed_version) == 1:
                upgradable_packages.append(pkg)

        if not upgradable_packages:
            pr.p(ansi.green + 'all of packages are up to date' + ansi.reset)
            return 0

        packages_names = [pkg.data['name'] for pkg in upgradable_packages]

        install_cmd = InstallCommand()
        return install_cmd.handle(ArgParser.parse(['cati', 'install', *self.args['options'], *packages_names]))
