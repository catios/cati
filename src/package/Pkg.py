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
import json
from frontend import Env
from frontend.SysArch import sys_arch
from package.exceptions import CannotReadFileException
from packaging import version

class Pkg:
    ''' Package model '''

    def __init__(self, data: dict):
        self.data = data
        try:
            self.data['repo']
        except:
            self.data['repo'] = 'Local'

    def installed(self):
        ''' Checks current package is installed '''
        if not Pkg.is_installed(self.data['name']):
            return False

        return Pkg.installed_version(self.data['name'])

    def get_depends(self):
        ''' Returns package dependencies list '''
        try:
            return self.data['depends']
        except:
            return []

    def get_conflicts(self):
        ''' Returns package conflicts list '''
        try:
            return self.data['conflicts']
        except:
            return []

    def get_reverse_depends(self) -> list:
        ''' Returns list of packages has dependency to this package '''
        reverse_depends = []
        for pkg in self.all_list()['list']:
            for dep in pkg.get_depends():
                if dep.strip().split(' ')[0] == self.data['name']:
                    reverse_depends.append(pkg)
        return reverse_depends

    @staticmethod
    def load_last(pkg_name: str):
        ''' Load last version of package by name '''
        pkgs_list = Pkg.all_list()
        for item in pkgs_list['list']:
            if item.data['name'] == pkg_name:
                return item
        return False

    @staticmethod
    def is_installed(package_name: str):
        ''' Gets a package name and checks is installed or not '''
        try:
            assert os.path.isdir(Env.installed_lists('/' + package_name))
            assert os.path.isfile(Env.installed_lists('/' + package_name + '/ver'))
            assert os.path.isfile(Env.installed_lists('/' + package_name + '/files'))
            # TODO : check more files

            return True
        except:
            return False

    @staticmethod
    def is_installed_manual(package_name):
        if not Pkg.is_installed(package_name):
            return False
        return os.path.isfile(Env.installed_lists('/' + package_name + '/manual'))

    @staticmethod
    def installed_version(package_name: str):
        ''' Gets name of package and returns installed version of that '''
        try:
            f = open(Env.installed_lists('/' + package_name + '/ver'), 'r')
            version = f.read()
            f.close()
        except:
            raise CannotReadFileException('cannot read file "' + Env.installed_lists('/' + package_name + '/ver') + '"')
        return version

    @staticmethod
    def installed_list():
        ''' Returns list of only installed packages '''
        all_packages = Pkg.all_list()
        installed_packages = {
            'errors': all_packages['errors'],
            'list': [],
        }
        for pkg in all_packages['list']:
            if pkg.installed():
                installed_packages['list'].append(pkg)

        return installed_packages

    @staticmethod
    def all_list():
        ''' Returns list of packages '''

        errors = []
        packages = []

        for item in os.listdir(Env.packages_lists()):
            if os.path.isfile(Env.packages_lists('/' + item + '/index')):
                f_index = open(Env.packages_lists('/' + item + '/index'), 'r')
                try:
                    index_content = f_index.read()
                    try:
                        index_json = json.loads(index_content)
                        try:
                            pkg = Pkg.load_from_index(index_json, item)
                            packages.append(pkg)
                        except:
                            errors.append('faild to load package "' + item + '"')
                    except:
                        errors.append('invalid json content in "' + Env.packages_lists('/' + item + '/index') + '"')
                except:
                    errors.append('cannot read file "' + Env.packages_lists('/' + item + '/index') + '"')
            else:
                errors.append(f'package "{item}" has not index file in lists ({Env.packages_lists("/" + item + "/index")} not found)')

        return {'list': packages, 'errors': errors}

    @staticmethod
    def compare_version(a, b):
        '''
        Compares two versions
        if 1 is returned means a is upper than b
        if 0 is returned means a equals b
        if -1 is returned means a is less than b
        '''
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
            if Pkg.compare_version(version, max_ver) == 1:
                max_ver = version

        return max_ver

    @staticmethod
    def load_from_index(index_json: dict, package_name: str):
        ''' Loads package data from index file '''
        try:
            arch = sys_arch()
            versions = index_json[arch]
        except:
            try:
                arch = 'all'
                versions = index_json[arch]
            except:
                arch = list(index_json.keys())[0]
                versions = index_json[arch]

        # load latest version
        ver = Pkg.get_last_version(versions)

        f = open(Env.packages_lists('/' + package_name + '/' + ver + '-' + arch), 'r')
        content = f.read()
        f.close()

        content_json = json.loads(content)

        return Pkg(content_json)

    def check_state(query_string: str) -> bool:
        '''
        Checks package state by query string

        For examples:
        "somepackage >= 1.5"
        "somepackage"
        "somepackage = 2.0"
        "somepackage < 1.7"
        "pkga | pkgb >= 1.0"
        "pkga | pkgb | pkgc"
        "pkga | pkgb & pkgc = 1.0"
        '''

        # parse query string
        parts = query_string.strip().split('|')
        orig_parts = []
        for part in parts:
            tmp = part.strip().split('&')
            orig_parts.append(tmp)
        
        # parse once query
        i = 0
        while i < len(orig_parts):
            j = 0
            while j < len(orig_parts[i]):
                orig_parts[i][j] = orig_parts[i][j].strip()
                spliter = None
                if '>=' in orig_parts[i][j]:
                    spliter = '>='
                elif '>=' in orig_parts[i][j]:
                    spliter = '<='
                elif '>' in orig_parts[i][j]:
                    spliter = '>'
                elif '<' in orig_parts[i][j]:
                    spliter = '<'
                elif '=' in orig_parts[i][j]:
                    spliter = '='
                if spliter != None:
                    orig_parts[i][j] = orig_parts[i][j].split(spliter)
                    orig_parts[i][j].insert(1, spliter)
                else:
                    orig_parts[i][j] = [orig_parts[i][j]]
                z = 0
                while z < len(orig_parts[i][j]):
                    orig_parts[i][j][z] = orig_parts[i][j][z].strip()
                    z += 1
                j += 1
            i += 1

        # check query
        for tmp in orig_parts:
            ands_ok = True
            for p in tmp:
                if len(p) == 1:
                    if not Pkg.is_installed(p[0]):
                        ands_ok = False
                elif len(p) == 3:
                    if not Pkg.is_installed(p[0]):
                        ands_ok = False
                    else:
                        a_ver = Pkg.installed_version(p[0])
                        b_ver = p[2]
                        if p[1] == '=':
                            if Pkg.compare_version(a_ver, b_ver) != 0:
                                ands_ok = False
                        elif p[1] == '>':
                            if Pkg.compare_version(a_ver, b_ver) != 1:
                                ands_ok = False
                        elif p[1] == '<':
                            if Pkg.compare_version(a_ver, b_ver) != -1:
                                ands_ok = False
                        elif p[1] == '<=':
                            if Pkg.compare_version(a_ver, b_ver) != -1 and Pkg.compare_version(a_ver, b_ver) != 0:
                                ands_ok = False
                        elif p[1] == '>=':
                            if Pkg.compare_version(a_ver, b_ver) != 1 and Pkg.compare_version(a_ver, b_ver) != 0:
                                ands_ok = False
                        else:
                            ands_ok = False
            if ands_ok:
                return True

        return False
