#
# RDependsCommand.py
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

""" RDepends command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.dotcati.Pkg import Pkg
from cati.cmdline.components import PackageShower

class RDependsCommand(BaseCommand):
    """ RDepends command """
    def help(self):
        """
        shows reverse depends list of packages

        this command shows which packages has dependency to an package

        Usage: cati rdepends pkg1 pkg2 ... [options]

        Options:
        -q|--quiet: quiet output
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'rdepends',
            'options': {
                '-q': [False, False],
                '--quiet': [False, False],
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def run(self):
        """ Run command """

        if not self.is_quiet():
            pr.p('Loading packages list...')
            pr.p('========================')

        loaded_packages = []

        for argument in self.arguments:
            pkg = Pkg.load_last(argument)
            if pkg:
                loaded_packages.append(pkg)
            else:
                self.message('unknow package "' + argument + '"' + ansi.reset, before=ansi.red)

        if not loaded_packages:
            return 1

        # show loaded packages
        for pkg in loaded_packages:
            # load reverse depends
            rdepends = pkg.get_reverse_depends()
            if not self.is_quiet():
                pr.p(pkg.data['name'] + ':')
            if not rdepends:
                if not self.is_quiet():
                    pr.p('  This package has not any reverse dependency')
            for item in rdepends:
                if not self.is_quiet():
                    pr.p('  ' + item.data['name'] + '=' + item.data['version'])
                else:
                    pr.p(item.data['name'] + '=' + item.data['version'])
            if len(loaded_packages) > 1:
                if not self.is_quiet():
                    pr.p('========================')
