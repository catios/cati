#
# ShowCommand.py
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

""" Show command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.dotcati.Pkg import Pkg
from cati.cmdline.components import PackageShower

class ShowCommand(BaseCommand):
    """ Show command """
    def help(self):
        """
        shows details of packages

        Usage: cati show pkg1 pkg2 ... [options]

        Options:
        --versions: shows versions list of packages
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'show',
            'options': {
                '--versions': [False, False],
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def run(self):
        """ Run command """

        pr.p('Loading packages list...')
        pr.p('========================')

        loaded_packages = []

        for argument in self.arguments:
            arg_parts = argument.split('=')
            if len(arg_parts) == 1:
                # load last version as default
                pkg = Pkg.load_last(argument)
            else:
                # load specify version
                pkg = Pkg.load_version(arg_parts[0], arg_parts[1])
                if pkg == 1:
                    pkg = False
                elif pkg == 2:
                    self.message('package "' + arg_parts[0] + '" has not version "' + arg_parts[1] + '"' + ansi.reset, before=ansi.red)
                    continue
            if pkg:
                loaded_packages.append(pkg)
            else:
                self.message('unknow package "' + argument + '"' + ansi.reset, before=ansi.red)

        if not loaded_packages:
            return 1

        # show loaded packages
        for pkg in loaded_packages:
            if self.has_option('--versions'):
                versions_list = pkg.get_versions_list()
                pr.p(pkg.data['name'] + ':')
                for ver in versions_list:
                    pr.p(' ' + ver[0] + ':' + ver[1])
            else:
                PackageShower.show(pkg.data)
            if len(loaded_packages) > 1:
                pr.p('---------------------')
