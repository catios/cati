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

import os, json
from frontend import Env
from frontend.SysArch import sys_arch
from package.exceptions.CannotReadFileException import CannotReadFileException
from packaging import version

class Pkg:
    ''' Package model '''

    def __init__(self , data: dict):
        self.data = data
        try:
            self.data['repo']
        except:
            self.data['repo'] = 'Local'

    def installed(self):
        if not Pkg.is_installed(self.data['name']):
            return False
        
        return Pkg.installed_version(self.data['name'])
    
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
        ''' Gets name of package and returns installed version of that '''
        try:
            f = open(Env.installed_lists('/' + package_name + '/ver') , 'r')
            version = f.read()
            f.close()
        except:
            raise CannotReadFileException('cannot read file "' + Env.installed_lists('/' + package_name + '/ver') + '"')
        return version

    @staticmethod
    def all_list():
        ''' Returns list of packages '''

        errors = []
        packages = []

        for item in os.listdir(Env.packages_lists()):
            if os.path.isfile(Env.packages_lists('/' + item + '/index')):
                f_index = open(Env.packages_lists('/' + item + '/index') , 'r')
                try:
                    index_content = f_index.read()
                    try:
                        index_json = json.loads(index_content)
                        try:
                            pkg = Pkg.load_from_index(index_json , item)
                            packages.append(pkg)
                        except:
                            errors.append('faild to load package "' + item + '"')    
                    except:
                        errors.append('invalid json content in "' + Env.packages_lists('/' + item + '/index') + '"')
                except:
                    errors.append('cannot read file "' + Env.packages_lists('/' + item + '/index') + '"')
            else:
                errors.append(f'package "{item}" has not index file in lists ({Env.packages_lists("/" + item + "/index")} not found)')

        return {'list': packages , 'errors': errors}

    @staticmethod
    def compare_version(a , b):
        a = version.parse(a)
        b = version.parse(b)

        if a > b:
            return 1

        if a == b:
            return 0

        if a < b:
            return -1

    @staticmethod
    def get_last_version(versions: list):
        ''' Gets a list from versions and returns latest version in that list '''
        max_ver = ''
        for version in versions:
            if Pkg.compare_version(version , max_ver) == 1:
                max_ver = version

        return max_ver

    @staticmethod
    def load_from_index(index_json: dict , package_name: str):
        ''' Loads package data from index file '''
        try:
            arch = sys_arch()
            versions = index_json[arch]
        except:
            arch = list(index_json.keys())[0]
            versions = index_json[arch]

        # load latest version
        ver = Pkg.get_last_version(versions)

        f = open(Env.packages_lists('/' + package_name + '/' + ver + '-' + arch) , 'r')
        content = f.read()
        f.close()

        content_json = json.loads(content)

        return Pkg(content_json)
