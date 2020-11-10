#
# FilesCommand.py
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

""" Files command """

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi
from package.Pkg import Pkg

class FilesCommand(BaseCommand):
    """ Files command """
    def help(self):
        """
        shows files list of packages
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'list',
            'options': {
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

        # show files list of loaded packages
        for pkg in loaded_packages:
            try:
                files_list = pkg.data['files']
            except:
                files_list = []
            pr.p(pkg.data['name'] + ':')
            if not files_list:
                pr.p(ansi.yellow + '  This package is empty' + ansi.reset)
            for item in files_list:
                pr.p('  ' + item)
            if len(loaded_packages) > 1:
                pr.p('========================')
