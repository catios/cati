#
# Pkg.py
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

""" Package model """

import os
import json
from cati.frontend import Env
from cati.frontend.SysArch import sys_arch
from .exceptions import CannotReadFileException
from packaging import version
from cati.helpers.hash import calc_file_sha256

class Pkg:
    """ Package model """

    def __init__(self, data: dict):
        self.data = data
        try:
            self.data['repo']
        except:
            self.data['repo'] = 'Local'
        self.data['version'] = self.data['version'].strip()

    def installed(self) -> (str, bool):
        """ Checks current package is installed. if yes, returns installed version and if not, returns False """
        if not Pkg.is_installed(self.data['name']):
            return False

        return Pkg.installed_version(self.data['name'])

    def installed_static_files(self) -> list:
        """
        returns list of installed files of package

        Returns:
            list[str]: files paths
        """
        if not self.installed():
            return False
        installed_static_files_list = open(Env.installed_lists('/' + self.data['name'] + '/staticfiles'), 'r').read().strip()
        installed_static_files_list = installed_static_files_list.split('\n')
        installed_static_files_list = [item.strip().split('@', 1) for item in installed_static_files_list if item.strip() != '']
        return installed_static_files_list

    def get_depends(self) -> list:
        """ Returns package dependencies list """
        try:
            return self.data['depends']
        except:
            return []

    def get_recommends(self) -> list:
        """ Returns package recommends list """
        try:
            return self.data['recommends']
        except:
            return []

    def get_conflicts(self) -> list:
        """ Returns package conflicts list """
        try:
            return self.data['conflicts']
        except:
            return []

    def get_replaces(self) -> list:
        """ Returns package replaces list """
        try:
            return self.data['replaces']
        except:
            return []

    def get_conffiles(self) -> list:
        """ Returns package conffiles list """
        try:
            return self.data['conffiles']
        except:
            return []

    def get_static_files(self) -> list:
        """ returns package static files list """
        try:
            return self.data['staticfiles']
        except:
            return []

    def get_reverse_depends(self) -> list:
        """ Returns list of packages has dependency to this package
        
        Returns:
            list[Pkg]: list of packages has dependency to this package
        """
        try:
            rd_pkgs_list_f = open(Env.packages_lists('/' + self.data['name'] + '/reverse_depends'), 'r')
            rd_pkgs_list = rd_pkgs_list_f.read().strip().split('\n')
            rd_pkgs_list_f.close()
        except:
            rd_pkgs_list = []
        rd_pkgs = []
        for item in rd_pkgs_list:
            if Pkg.is_installed(item):
                rd_pkgs.append(Pkg.load_version(item, Pkg.installed_version(item)))
            else:
                rd_pkgs.append(Pkg.load_last(item))
        reverse_depends = []
        for pkg in rd_pkgs:
            if pkg.installed():
                pkg = Pkg.load_version(pkg.data['name'], pkg.installed())
            for dep in pkg.get_depends():
                if dep.strip()[0] != '@':
                    result = Pkg.check_state(dep, virtual={
                        'remove': [
                            [
                                self.data['name'], self.data['version']
                            ]
                        ],
                        'all_real_is_installed': True
                    })
                    if not result:
                        reverse_depends.append(pkg)
        return reverse_depends

    def get_reverse_conflicts(self) -> list:
        """ Returns list of packages has conflicts with this package
        
        Returns:
            list[Pkg]: list of packages has conflict with this package"""
        try:
            rd_pkgs_list_f = open(Env.packages_lists('/' + self.data['name'] + '/reverse_conflicts'), 'r')
            rd_pkgs_list = rd_pkgs_list_f.read().strip().split('\n')
            rd_pkgs_list_f.close()
        except:
            rd_pkgs_list = []
        rd_pkgs = []
        for item in rd_pkgs_list:
            if Pkg.is_installed(item):
                rd_pkgs.append(Pkg.load_version(item, Pkg.installed_version(item)))
        reverse_conflicts_list = []
        for pkg in rd_pkgs:
            conflicts = pkg.get_conflicts()
            for conflict in conflicts:
                result = Pkg.check_state(conflict, {'install': [
                    [
                        self.data['name'], self.data['version']
                    ]
                ], 'no_real_installs': True})
                if result:
                    pkg.conflict_error = conflict
                    reverse_conflicts_list.append(pkg)
        return reverse_conflicts_list

    def get_file_size_str(self) -> str:
        """
        Returns file size of the package as str (for example `32 MB`)

        Returns:
            str: file size str
        """
        try:
            file_size = self.data['file_size']
        except:
            file_size = 0

        return Pkg.get_download_size_str(file_size)

    @staticmethod
    def get_download_size_str(dsize: int) -> str:
        """
        Returns file size str from bytes interger

        Args:
            dsize: bytes count

        Returns:
            str: download str
        """
        return str(dsize) + ' B'

    def get_versions_list(self):
        """
        returns versions list of the package
        
        Returns:
            list: list of versions: [ [<version>, <arch>] ]
        """
        try:
            f_index = open(Env.packages_lists('/' + self.data['name'] + '/index'), 'r')
            index_json = json.loads(f_index.read())
            f_index.close()
        except:
            return []
        
        try:
            versions = []
            for k in index_json:
                for ver in index_json[k]:
                    versions.append([ver, k])
            return versions
        except:
            return []

    @staticmethod
    def get_all_installed_files_list() -> list:
        """
        returns list of all of installed files

        Returns:
            list: [
                ['pkgname', 'filetype(d,f,cd,cf)', '/file/path'],
                ['pkg1', 'f', '/path/to/file'],
                ...
            ]
        """
        # load list of installed packages
        installed_packages = Pkg.installed_list()['list']
        result = []
        for pkg in installed_packages:
            pkg_installed_files = open(Env.installed_lists('/' + pkg.data['name'] + '/files'), 'r').read()
            pkg_installed_files = pkg_installed_files.strip().split('\n')
            pkg_installed_files = [item.strip().split(':', 1) for item in pkg_installed_files]
            for f in pkg_installed_files:
                if len(f) > 1:
                    result.append([pkg.data['name'], f[0], f[1]])
        return result

    @staticmethod
    def load_last(pkg_name: str) -> bool:
        """ Load last version of package by name

        Args:
            pkg_name (str): the package name

        Returns:
            bool (False): package not found
            Pkg: the loaded Pkg boject
        """
        pkgs_list = Pkg.all_list()
        for item in pkgs_list['list']:
            if item.data['name'] == pkg_name:
                return item
        return False

    @staticmethod
    def is_installed(package_name: str) -> bool:
        """ Gets a package name and checks is installed or not
        
        Args:
            package_name (str): the package name you want to check is installed
        
        Returns:
            bool
        """
        try:
            assert os.path.isdir(Env.installed_lists('/' + package_name))
            assert os.path.isfile(Env.installed_lists('/' + package_name + '/ver'))
            assert os.path.isfile(Env.installed_lists('/' + package_name + '/files'))
            return True
        except:
            return False

    @staticmethod
    def is_installed_manual(package_name: str) -> bool:
        """ Gets a package name and checks is installed MANUAL or not
        
        Args:
            package_name (str): the package name you want to check is installed
        
        Returns:
            bool
        """
        if not Pkg.is_installed(package_name):
            return False
        return os.path.isfile(Env.installed_lists('/' + package_name + '/manual'))

    @staticmethod
    def load_version(pkg_name: str, version: str, arch=''):
        """
        loads a specify version of a package

        Args:
            pkg_name (str): name of package
            version (str): that version you want to load
            arch (str): load specify arch (optional)
        
        Returns:
            int (1): package not found
            int (2): package found, but version/arch not found
            Pkg object: package and version found and returned
        """
        if not os.path.isfile(Env.packages_lists('/' + pkg_name + '/index')):
            return 1

        # load package index file
        f_index = open(Env.packages_lists('/' + pkg_name + '/index'), 'r')
        index_content = f_index.read()
        f_index.close()

        try:
            # load json
            index = json.loads(index_content)
        except:
            return 1

        # load package versions list
        versions = []
        try:
            versions = index[arch]
        except:
            try:
                versions = index[SysArch.sys_arch()]
                arch = SysArch.sys_arch()
            except:
                try:
                    versions = index['all']
                    arch = 'all'
                except:
                    versions = index[list(index.keys())[0]]
                    arch = list(index.keys())[0]

        for ver in versions:
            if ver == version:
                # load this version data
                try:
                    f_ver = open(Env.packages_lists('/' + pkg_name + '/' + ver + '-' + arch), 'r')
                    f_ver_content = f_ver.read()
                    ver_data = json.loads(f_ver_content)
                    return Pkg(ver_data)
                except:
                    return 2
        return 2

    @staticmethod
    def installed_version(package_name: str) -> str:
        """ Gets name of package and returns installed version of that
        
        Args:
            package_name (str): name of package
        
        Returns:
            str: installed version
        
        Raises:
            package.exceptions.CannotReadFileException: when cannot read package database files
        """
        try:
            f = open(Env.installed_lists('/' + package_name + '/ver'), 'r')
            version = f.read()
            f.close()
        except:
            raise CannotReadFileException('cannot read file "' + Env.installed_lists('/' + package_name + '/ver') + '"')
        return version

    @staticmethod
    def installed_list() -> dict:
        """ Returns list of only installed packages 
        
        Returns:
            dict: output has two keys:
                  {
                      "list": list[Pkg] // list of packages
                      "errors": list // errors while loading packages
                  }
        """
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
        """ Returns list of packages
        
        Returns:
            dict: output has two keys:
                  {
                      "list": list[Pkg] // list of packages
                      "errors": list // errors while loading packages
                  }
        """

        errors = []
        packages = []

        tmp_list = os.listdir(Env.packages_lists())
        tmp_list.sort()
        for item in tmp_list:
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
                            if not (os.path.isfile(Env.packages_lists('/' + item + '/reverse_depends')) or os.path.isfile(Env.packages_lists('/' + item + '/reverse_conflicts'))):
                                errors.append('faild to load package "' + item + '"')
                    except:
                        errors.append('invalid json content in "' + Env.packages_lists('/' + item + '/index') + '"')
                except:
                    errors.append('cannot read file "' + Env.packages_lists('/' + item + '/index') + '"')
            else:
                errors.append(f'package "{item}" has not index file in lists ({Env.packages_lists("/" + item + "/index")} not found)')

        return {'list': packages, 'errors': errors}

    @staticmethod
    def compare_version(a: str, b: str):
        """
        Compares two versions.

        Args:
            a (str): first version
            b (str): second version
        
        Returns:
            if 1 is returned means a is upper than b.
            if 0 is returned means a equals b.
            if -1 is returned means a is less than b.
        """
        a = version.parse(a)
        b = version.parse(b)

        if a > b:
            return 1

        if a == b:
            return 0

        if a < b:
            return -1

    @staticmethod
    def get_last_version(versions: list) -> str:
        """ Gets a list from versions and returns latest version in that list
        
        Args:
            versions (list[str]): list of versions you want find last of them
        
        Returns:
            str: the last version in the list
        """
        max_ver = ''
        for version in versions:
            if Pkg.compare_version(version, max_ver) == 1:
                max_ver = version

        return max_ver

    @staticmethod
    def load_from_index(index_json: dict, package_name: str):
        """ Loads package data from index file
        
        Args:
            package_name (str): name of the package
            index_json (dict): loaded json data from `/var/lib/cati/lists/<pkgname>/index` file

        Returns:
            Pkg: the loaded Pkg object
        """
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

    def check_state(query_string: str, virtual=None, get_false_pkg=False, get_false_pkg_next=0, get_true_pkg=False, get_true_pkg_next=0, only_parse=False) -> bool:
        """
        Checks package state by query string.

        Examples:
        "somepackage >= 1.5",
        "somepackage",
        "somepackage = 2.0",
        "somepackage < 1.7",
        "pkga | pkgb >= 1.0",
        "pkga | pkgb | pkgc",
        "pkga | pkgb & pkgc = 1.0",

        also there is a feature to check files:

        "@/usr/bin/somefile",
        "somepackage | @/path/to/somefile",
        "testpkga >= 3.0 | @/somefile"
        "@/file/one | @/file/two",
        "@<sha256-hash>@/path/to/file",
        "@76883f0fd14015c93296f0e4202241f4eb3a23189dbc17990a197477f1dc441a@/path/to/file"

        `virtual` argument:

        this argument can make a virtual package state
        for example package `testpkgz` is not installed,
        but we want to check the query when this is installed
        we can set that package in virtual system to query checker
        calculate tha package as installed/removed
        virtual structure: this is dictonary:
        {
            'install': [
                ## a list from installed packages:
                ['testpkgx', '1.0'],
                ['testpkgz', '3.7.11'],
                ...
            ]

            'remove': [
                ## a list from removed packages:
                ['testpkgx', '1.0'],
                ['testpkgz', '3.7.11'],
                ...
            ]

            ## set it True if you want to ignore real installations
            'no_real_installs': True/False

            ## set it True if you want to ignore real not installations
            'all_real_is_installed': True/False
        }
        """

        # parse query string
        parts = query_string.strip().split('|')
        orig_parts = []
        for part in parts:
            tmp = part.strip().split('&')
            orig_parts.append(tmp)

        # load virtual item
        no_real_installs = False
        all_real_is_installed = False
        if virtual:
            try:
                tmp = virtual['install']
            except:
                virtual['install'] = []
            try:
                tmp = virtual['remove']
            except:
                virtual['remove'] = []
            virtual_installed_names_list = []
            virtual_installed_versions_dict = {}
            for item in virtual['install']:
                virtual_installed_versions_dict[item[0]] = item[1]
                virtual_installed_names_list.append(item[0])
            virtual_removed_names_list = []
            virtual_removed_versions_dict = {}
            for item in virtual['remove']:
                virtual_removed_versions_dict[item[0]] = item[1]
                virtual_removed_names_list.append(item[0])
            try:
                no_real_installs = virtual['no_real_installs']
            except:
                no_real_installs = False
            try:
                all_real_is_installed = virtual['all_real_is_installed']
            except:
                all_real_is_installed = False
        else:
            virtual_installed_names_list = []
            virtual_installed_versions_dict = {}
            virtual_removed_names_list = []
            virtual_removed_versions_dict = {}
            no_real_installs = False
            all_real_is_installed = False

        # parse once query
        i = 0
        while i < len(orig_parts):
            j = 0
            while j < len(orig_parts[i]):
                orig_parts[i][j] = orig_parts[i][j].strip()
                spliter = None
                if '>=' in orig_parts[i][j]:
                    spliter = '>='
                elif '<=' in orig_parts[i][j]:
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

        if only_parse:
            return orig_parts

        # check query
        for tmp in orig_parts:
            ands_ok = True
            for p in tmp:
                if p[0][0] == '@':
                    # check file query
                    parts = p[0].split('@')
                    if len(parts) == 2:
                        if not os.path.exists(Env.base_path(parts[-1])):
                            ands_ok = False
                    elif len(parts) == 3:
                        if not os.path.exists(Env.base_path(parts[-1])):
                            ands_ok = False
                        else:
                            if os.path.isfile(Env.base_path(parts[-1])):
                                sha256_sum = calc_file_sha256(Env.base_path(parts[-1]))
                                if parts[1] != sha256_sum:
                                    ands_ok = False
                elif not p[0] in virtual_installed_names_list and no_real_installs:
                    ands_ok = False
                    if get_false_pkg and get_false_pkg_next <= 0:
                        return p
                    else:
                        get_false_pkg_next -= 1
                elif not p[0] in virtual_removed_names_list and all_real_is_installed:
                    pass
                elif len(p) == 1:
                    if not Pkg.is_installed(p[0]) and not p[0] in virtual_installed_names_list or p[0] in virtual_removed_names_list:
                        ands_ok = False
                        if get_false_pkg and get_false_pkg_next <= 0:
                            return p
                        else:
                            get_false_pkg_next -= 1
                elif len(p) == 3:
                    if not Pkg.is_installed(p[0]) and not p[0] in virtual_installed_names_list or p[0] in virtual_removed_names_list:
                        ands_ok = False
                        if get_false_pkg and get_false_pkg_next <= 0:
                            return p
                        else:
                            get_false_pkg_next -= 1
                    else:
                        if p[0] in virtual_installed_names_list:
                            a_ver = virtual_installed_versions_dict[p[0]]
                        else:
                            a_ver = Pkg.installed_version(p[0])
                        b_ver = p[2]
                        if p[1] == '=':
                            if Pkg.compare_version(a_ver, b_ver) != 0:
                                ands_ok = False
                                if get_false_pkg and get_false_pkg_next <= 0:
                                    return p
                                else:
                                    get_false_pkg_next -= 1
                        elif p[1] == '>':
                            if Pkg.compare_version(a_ver, b_ver) != 1:
                                ands_ok = False
                                if get_false_pkg and get_false_pkg_next <= 0:
                                    return p
                                else:
                                    get_false_pkg_next -= 1
                        elif p[1] == '<':
                            if Pkg.compare_version(a_ver, b_ver) != -1:
                                ands_ok = False
                                if get_false_pkg and get_false_pkg_next <= 0:
                                    return p
                                else:
                                    get_false_pkg_next -= 1
                        elif p[1] == '<=':
                            if Pkg.compare_version(a_ver, b_ver) != -1 and Pkg.compare_version(a_ver, b_ver) != 0:
                                ands_ok = False
                                if get_false_pkg and get_false_pkg_next <= 0:
                                    return p
                                else:
                                    get_false_pkg_next -= 1
                        elif p[1] == '>=':
                            if Pkg.compare_version(a_ver, b_ver) != 1 and Pkg.compare_version(a_ver, b_ver) != 0:
                                ands_ok = False
                                if get_false_pkg and get_false_pkg_next <= 0:
                                    return p
                                else:
                                    get_false_pkg_next -= 1
                        else:
                            ands_ok = False
                            if get_false_pkg and get_false_pkg_next <= 0:
                                return p
                            else:
                                get_false_pkg_next -= 1
                if ands_ok and get_true_pkg and get_true_pkg_next <= 0:
                    return p
                else:
                    get_true_pkg_next -= 1
            if ands_ok:
                return True

        return False
