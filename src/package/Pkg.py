#
# Pkg.py
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

''' Package model '''

import os
from frontend import Env
from package.exceptions.CannotReadFileException import CannotReadFileException

class Pkg:
    ''' Package model '''
    
    @staticmethod
    def is_installed(package_name: str):
        try:
            assert os.path.isdir(Env.installed_lists('/' + package_name))
            assert os.path.isfile(Env.installed_lists('/' + package_name + '/ver'))
            assert os.path.isfile(Env.installed_lists('/' + package_name + '/files'))
            # TODO : check more files

            return True
        except:
            return False

    @staticmethod
    def installed_version(package_name: str):
        try:
            f = open(Env.installed_lists('/' + package_name + '/ver') , 'r')
            version = f.read()
            f.close()
        except:
            raise CannotReadFileException('cannot read file "' + Env.installed_lists('/' + package_name + '/ver') + '"')
        return version
