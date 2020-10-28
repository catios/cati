#
# Installer.py
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

''' Dotcati package installer '''

import os
import json
import time
from dotcati.ArchiveModel import ArchiveModel
from frontend import Env, Temp, SysArch
from dotcati import ListUpdater
from package.Pkg import Pkg
from dotcati.exceptions import DependencyError, ConflictError
from transaction.BaseTransaction import BaseTransaction

class Installer:
    ''' Dotcati package installer '''

    def load_files(self, path: str, base_temp_path: str):
        ''' Loads list of package files from extracted temp dir '''

        for item in os.listdir(path):
            if os.path.isfile(path + '/' + item):
                self.loaded_files.append([(path + '/' + item)[len(base_temp_path):], path + '/' + item])
            else:
                self.loaded_files.append([(path + '/' + item)[len(base_temp_path):], path + '/' + item])
                self.load_files(path + '/' + item, base_temp_path)

    def copy_once_file(self, paths):
        ''' Copy one of package files '''
        if os.path.isfile(paths[1]):
            os.system('cp "' + paths[1] + '" "' + Env.base_path(paths[0]) + '"')
            self.copied_files.append('f:' + paths[0])
        else:
            os.mkdir(Env.base_path(paths[0]))
            self.copied_files.append('d:' + paths[0])

    def copy_files(self, pkg: ArchiveModel, directory_not_empty_event) -> list:
        ''' Copy package files on system '''
        # load package old files list
        old_files = []
        if os.path.isfile(Env.installed_lists('/' + pkg.data['name'] + '/files')):
            try:
                f = open(Env.installed_lists('/' + pkg.data['name'] + '/files'), 'r')
                for line in f.read().strip().split('\n'):
                    if line != '':
                        old_files.append(line.strip())
            except:
                pass
        old_files = list(reversed(old_files))

        # extract package in a temp place
        temp_dir = Temp.make_dir()
        os.rmdir(temp_dir)
        try:
            pkg.extractall(temp_dir)
        except IsADirectoryError:
            pass

        # load files list from `files` directory of package
        self.loaded_files = []
        self.load_files(temp_dir + '/files', temp_dir + '/files')

        # copy loaded files
        self.copied_files = []
        for f in self.loaded_files:
            if os.path.exists(Env.base_path(f[0])):
                if os.path.isfile(Env.base_path(f[0])):
                    if ('f:' + f[0]) in old_files:
                        self.copy_once_file(f)
                        old_files.pop(old_files.index(('f:' + f[0])))
                else:
                    if ('d:' + f[0]) in old_files:
                        self.copied_files.append('d:' + f[0])
                        old_files.pop(old_files.index(('d:' + f[0])))
            else:
                self.copy_once_file(f)

        # delete not wanted old files
        for item in old_files:
            parts = item.strip().split(':', 1)
            if parts[0] == 'cf' or parts[0] == 'cd':
                pass
            else:
                if os.path.isfile(parts[1]):
                    os.remove(parts[1])
                else:
                    try:
                        os.rmdir(parts[1])
                    except:
                        # directory is not emptyr
                        directory_not_empty_event(pkg, parts[1])

        return self.copied_files

    def check_dep_and_conf(self, pkg: ArchiveModel):
        ''' Checks package dependencies and conflicts '''

        # load package dependencies
        try:
            depends = pkg.data['depends']
        except:
            depends = []

        # load package conflicts
        try:
            conflicts = pkg.data['conflicts']
        except:
            conflicts = []

        for dep in depends:
            if not Pkg.check_state(dep):
                raise DependencyError(dep)

        for conflict in conflicts:
            if Pkg.check_state(conflict):
                raise ConflictError(conflict)

    def install(self, pkg: ArchiveModel, index_updater_events: dict, installer_events: dict):
        '''
        Install .cati package

        installer_events:
        - package_currently_install: gets a current installed version
        - package_new_installs: gets package archive
        - package_installed: will call after package installation
        - dep_and_conflict_error: will run when there is depends or conflict error
        - arch_error: will run when package arch is not sync with sys arch
        '''

        # check package architecture
        if pkg.data['arch'] != 'all':
            if SysArch.sys_arch() != pkg.data['arch']:
                return installer_events['arch_error'](pkg)

        # check package dependencies and conflicts
        try:
            self.check_dep_and_conf(pkg)
        except DependencyError as ex:
            return installer_events['dep_and_conflict_error'](pkg, ex)
        except ConflictError as ex:
            return installer_events['dep_and_conflict_error'](pkg, ex)

        # add package to state
        state_f = open(Env.state_file(), 'w')
        state_f.write('install%' + pkg.data['name'] + '%' + pkg.data['version'] + '%' + pkg.data['arch'] + '\n')
        state_f.close()

        # add package data to lists
        if not os.path.isdir(Env.packages_lists('/' + pkg.data['name'])):
            os.mkdir(Env.packages_lists('/' + pkg.data['name']))

        lists_path = Env.packages_lists('/' + pkg.data['name'] + '/' + pkg.data['version'] + '-' + pkg.data['arch'])

        try:
            lists_f = open(lists_path, 'r')
            old_repo = json.loads(lists_f.read())['repo']
            lists_f.close()
        except:
            old_repo = 'Local'
            pass

        lists_f = open(lists_path, 'w')
        pkg.data['repo'] = old_repo
        lists_f.write(json.dumps(pkg.data))
        lists_f.close()

        ListUpdater.update_indexes(index_updater_events)

        # install package
        if Pkg.is_installed(pkg.data['name']):
            installer_events['package_currently_installed'](pkg, Pkg.installed_version(pkg.data['name']))
        else:
            installer_events['package_new_installs'](pkg)

        copied_files = self.copy_files(pkg, installer_events['directory_not_empty'])

        # set install configuration
        if not os.path.isdir(Env.installed_lists('/' + pkg.data['name'])):
            os.mkdir(Env.installed_lists('/' + pkg.data['name']))
        f_ver = open(Env.installed_lists('/' + pkg.data['name'] + '/ver'), 'w')
        f_ver.write(pkg.data['version']) # write installed version
        f_ver.close()

        f_files = open(Env.installed_lists('/' + pkg.data['name'] + '/files'), 'w')
        copied_files_str = ''
        for copied_file in copied_files:
            copied_files_str += copied_file + '\n'
        f_files.write(copied_files_str.strip()) # write copied files
        f_files.close()

        f_installed_at = open(Env.installed_lists('/' + pkg.data['name'] + '/installed_at'), 'w')
        f_installed_at.write(str(time.time())) # write time (installed at)
        f_installed_at.close()

        # pop package from state
        BaseTransaction.pop_state()

        # call package installed event
        installer_events['package_installed'](pkg)
