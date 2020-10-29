#
# Remove.py
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

""" Remove transaction """

import os
import shutil
from transaction.BaseTransaction import BaseTransaction
from package.Pkg import Pkg
from frontend import Env

class Remove(BaseTransaction):
    """ Remove transaction """
    @staticmethod
    def run(pkg: Pkg, events: dict):
        """ Remove pkg """
        events['removing_package'](pkg)

        # remove package
        installed_files = open(Env.installed_lists('/' + pkg.data['name'] + '/files'), 'r').read()
        installed_files = installed_files.strip().split('\n')
        for f in installed_files:
            if f != '':
                f_type = f.strip().split(':', 1)[0]
                f_path = f.strip().split(':', 1)[1]
                if f_type == 'f':
                    if os.path.isfile(f_path):
                        os.remove(f_path)
                elif f_type == 'd':
                    try:
                        os.rmdir(f_path)
                    except:
                        events['dir_is_not_empty'](pkg, f)
                elif f_type == 'cf':
                    pass # TODO : handle conffiles
                elif f_type == 'cd':
                    pass

        # remove installation config
        shutil.rmtree(Env.installed_lists('/' + pkg.data['name']))

        events['package_remove_finished'](pkg)
