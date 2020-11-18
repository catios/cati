#
# ForgetCommand.py
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

""" Forget command """

import os
import shutil
import glob
from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi
from package.Pkg import Pkg
from frontend import Env, RootRequired
from dotcati import ListUpdater

class ForgetCommand(BaseCommand):
    """ Forget command """
    def help(self):
        """
        forgets packages from packages list

        Usage:
        - cati forget pkg1
        - cati forget pkg1=1.12.7
        - cati forget pkg1 pkg2 pkg3=1.0 pkg4 ...
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'show',
            'options': {
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def empty_method_for_event(a=None, b=None):
        """ an empty method """
        pass

    def run(self):
        """ Run command """

        RootRequired.require_root_permission()

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
                else:
                    pkg.only_specify_version = True
            if pkg:
                try:
                    pkg.only_specify_version
                except:
                    pkg.only_specify_version = False
                if pkg.installed():
                    if not pkg.only_specify_version:
                        self.message('package "' + argument + '" is installed. cannot forget installed packages' + ansi.reset, before=ansi.red)
                        continue
                    else:
                        if pkg.installed() == pkg.data['version']:
                            self.message('package ' + argument + ' (' + pkg.data['version'] + ') is installed. cannot forget installed packages' + ansi.reset, before=ansi.red)
                            continue
                loaded_packages.append(pkg)
            else:
                self.message('unknow package "' + argument + '"' + ansi.reset, before=ansi.red)

        if not loaded_packages:
            return 1

        # forget loaded packages
        for pkg in loaded_packages:
            if not pkg.only_specify_version:
                # forget all of package versions
                shutil.rmtree(Env.packages_lists('/' + pkg.data['name']))
                pr.p('Package ' + pkg.data['name'] + ' was forgoten successfully')
            else:
                # TODO : fix bug of this code:
                # for example if we want to delete version `1.0`,
                # and there is another version named `1.0-alpha`,
                # so, we have two files, `1.0-{arch}` and `1.0-alpha-{arch}`.
                # in this glob query, we will get both of them and both of them
                # will be deleted but we just want to delete `1.0` not `1.0-alpha`.
                # this bug have to be fixed
                files = glob.glob(Env.packages_lists('/' + pkg.data['name'] + '/' + pkg.data['version'] + '-*'))
                for f in files:
                    os.remove(f)
                pr.p('Version ' + pkg.data['version'] + ' of package ' + pkg.data['name'] + ' was forgoten successfully')
            try:
                if len(os.listdir(Env.packages_lists('/' + pkg.data['name']))) <= 1:
                    shutil.rmtree(Env.packages_lists('/' + pkg.data['name']))
            except:
                pass

        ListUpdater.update_indexes({
            'cannot_read_file': self.empty_method_for_event,
            'invalid_json_data': self.empty_method_for_event,
        })
