#
# Installer.py
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

""" Dotcati package installer """

import os
import json
import time
import hashlib
from .ArchiveModel import BaseArchive
from cati.frontend import Env, Temp, SysArch, SecurityBlacklist
from . import ListUpdater
from .Pkg import Pkg
from .exceptions import DependencyError, ConflictError, PackageScriptError, PackageIsInSecurityBlacklist, FileConflictError
from cati.transaction.BaseTransaction import BaseTransaction
from cati.helpers.hash import calc_file_sha256, calc_file_sha512, calc_file_md5

class Installer:
    """ Dotcati package installer """

    def load_files(self, path: str, base_temp_path: str):
        """
        Loads list of package files from extracted temp dir

        you should set `self.loaded_files` list before call this.
        this method will put loaded files in self.loaded_files list

        Args:
            path (str): that directory you want to load files list from that
            base_temp_path (str): base path of package extracted temp directory
        """

        for item in os.listdir(path):
            if os.path.isfile(path + '/' + item):
                self.loaded_files.append([(path + '/' + item)[len(base_temp_path):], path + '/' + item])
            else:
                self.loaded_files.append([(path + '/' + item)[len(base_temp_path):], path + '/' + item])
                self.load_files(path + '/' + item, base_temp_path)

    def copy_once_file(self, paths):
        """ Copy one of package files (this method is called from `copy_files` method) """
        if os.path.isfile(paths[1]):
            if paths[0] in self.conffiles:
                self.copied_files.append('cf:' + paths[0])
                old_conffiles = [item[-1] for item in self.old_conffiles]
                if paths[0] in old_conffiles:
                    f_hash = calc_file_sha256(paths[1])
                    if [f_hash, paths[0]] in self.old_conffiles:
                        self.uncopied_conffiles[paths[0]] = f_hash
                        return
                    else:
                        if self.keep_conffiles:
                            self.uncopied_conffiles[paths[0]] = f_hash
                            return
            else:
                self.copied_files.append('f:' + paths[0])
            os.system('cp "' + paths[1] + '" "' + Env.base_path(paths[0]) + '"')
        else:
            os.mkdir(Env.base_path(paths[0]))
            if paths[1] in self.conffiles:
                self.copied_files.append('cd:' + paths[0])
            else:
                self.copied_files.append('d:' + paths[0])

    def copy_files(self, pkg: BaseArchive, directory_not_empty_event, target_path='') -> list:
        """
        Copy package files on system

        Args:
            pkg (BaseArchive): the package archive object
            directory_not_empty_event (callable): the function will be run when we want to delete old direcotry
                                      of package and that is not empty.
            target_path (str): target path prefix of copied files location. default is `/` means
                               copies files on the root directory. you can change it.

        Returns:
            list[str]: list of copied files
        """
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

        # load unremoved conffiles list
        unremoved_conffiles_f = open(Env.unremoved_conffiles(), 'r')
        unremoved_conffiles = unremoved_conffiles_f.read().strip().split('\n')
        unremoved_conffiles_f.close()

        temp_dir = self.extracted_package_dir

        # load files list from `files` directory of package
        self.loaded_files = []
        self.load_files(temp_dir + '/files', temp_dir + '/files')
        self.loaded_files = [[target_path + f[0], f[1]] for f in self.loaded_files]

        # check file conflicts
        all_installed_files = Pkg.get_all_installed_files_list()
        for lf in self.loaded_files:
            if not os.path.isdir(lf[1]):
                for insf in all_installed_files:
                    if insf[0].split(':', 1)[0] != pkg.data['name']:
                        if lf[0] == insf[2]:
                            insf_pkg = Pkg.load_last(insf[0])
                            if insf_pkg:
                                insf[0] = insf[0] + ':' + insf_pkg.installed()
                            # check package is in `replaces` list
                            do_raise_error = True
                            replaces_list = pkg.get_replaces()
                            for rep in replaces_list:
                                if Pkg.check_state(rep):
                                    tmp_parts = rep.split(' ')
                                    tmp_parts = tmp_parts[0].split('>')
                                    tmp_parts = tmp_parts[0].split('<')
                                    tmp_parts = tmp_parts[0].split('=')
                                    tmp_parts = tmp_parts[0]
                                    if tmp_parts == insf[0].split(':', 1)[0]:
                                        do_raise_error = False
                            if do_raise_error:
                                raise FileConflictError(
                                    'package ' + pkg.data['name'] + ':' + pkg.data['version'] + ' and ' + insf[0] + ' both has file "' + lf[0] + '"'
                                )

        # copy loaded files
        self.copied_files = []
        for f in self.loaded_files:
            if os.path.exists(Env.base_path(f[0])):
                if os.path.isfile(Env.base_path(f[0])):
                    if ('f:' + f[0]) in old_files or ('cf:' + f[0]) in old_files:
                        self.copy_once_file(f)
                        try:
                            old_files.pop(old_files.index(('f:' + f[0])))
                        except:
                            pass
                    else:
                        if f[0] in unremoved_conffiles:
                            self.copy_once_file(f)
                            unremoved_conffiles.pop(unremoved_conffiles.index(f[0]))
                        else:
                            self.copy_once_file(f)
                else:
                    if ('d:' + f[0]) in old_files or ('cd:' + f[0]) in old_files:
                        if ('cd:' + f[0]) in old_files:
                            self.copied_files.append('cd:' + f[0])
                            old_files.pop(old_files.index(('cd:' + f[0])))
                        else:
                            self.copied_files.append('d:' + f[0])
                            old_files.pop(old_files.index(('d:' + f[0])))
                    else:
                        if f[0] in unremoved_conffiles:
                            self.copied_files.append('d:' + f[0])
                            unremoved_conffiles.pop(unremoved_conffiles.index(f[0]))
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

        # write new unremoved conffiles list
        unremoved_conffiles_f = open(Env.unremoved_conffiles(), 'w')
        new_content = ''
        for item in unremoved_conffiles:
            new_content += item + '\n'
        unremoved_conffiles_f.write(new_content)
        unremoved_conffiles_f.close()

        return self.copied_files

    def check_dep_and_conf(self, pkg: BaseArchive):
        """
        Checks package dependencies and conflicts.

        Args:
            pkg: (BaseArchive) the package archive object

        Raises:
            DependencyError: when a dependency is not installed (dependency will put in exception message)
            ConflictError: when a conflict is installed (conflict will put in exception message)
        """

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

        # load package reverse cconflicts (packages has conflict to this package)
        reverse_conflicts = pkg.get_reverse_conflicts()

        for dep in depends:
            if not Pkg.check_state(dep):
                raise DependencyError(dep)

        for conflict in conflicts:
            if Pkg.check_state(conflict):
                raise ConflictError(conflict)

        # check reverse conflicts
        if reverse_conflicts:
            raise ConflictError('reverse conflict with ' + reverse_conflicts[0].data['name'] + ': ' + reverse_conflicts[0].conflict_error)

    def run_script(self, script_name: str, script_path=None):
        """
        runs an script in the package (only install scripts)

        Args:
            script_name (str): name of that script you want to run
            script_path (str, None): you can change the default path of script file with this argument

        Raises:
            dotcati.exceptions.PackageScriptError: when script returns non-zero exit code
                (exit code will put in `error_code` attribute of exception object)
        """
        if script_path == None:
            script_path = self.extracted_package_dir + '/scripts/' + script_name
        if os.path.isfile(script_path):
            # script exists, run script
            os.system('chmod +x "' + script_path + '"')
            # run script and pass old version of package (if currently installed)
            old_version = ''
            try:
                old_version = self.old_version
            except:
                if Pkg.is_installed(self.pkg.data['name']):
                    self.old_version = '"' + Pkg.installed_version(self.pkg.data['name']) + '"'
                    old_version = self.old_version
            result = os.system(script_path + ' ' + old_version)
            if result != 0:
                tmp = PackageScriptError("script " + script_name + ' returned non-zero code ' + str(result))
                tmp.error_code = result
                raise tmp

    def check_security_blacklist(self, pkg: BaseArchive):
        """
        checks package sha256, sha512 and md5 and checks this hashes in security blacklist.

        Args:
            pkg (BaseArchive): the package archive object

        Raises:
            dotcati.exceptions.PackageIsInSecurityBlacklist: when package is blocked in security blacklist
                (the blacklist details will put in `blacklist_item` attribute of exception object)
        """
        # calculate hashes
        sha256 = calc_file_sha256(pkg.package_file_path)
        sha512 = calc_file_sha512(pkg.package_file_path)
        md5 = calc_file_md5(pkg.package_file_path)

        # check blacklist
        blacklist = SecurityBlacklist.get_list()
        for item in blacklist:
            if item['md5'] == md5 and item['sha512'] == sha512 and item['sha256'] == sha256:
                ex = PackageIsInSecurityBlacklist()
                ex.blacklist_item = item
                raise ex

    def install(self, pkg: BaseArchive, index_updater_events: dict, installer_events: dict, is_manual=True, run_scripts=True, target_path='', keep_conffiles=False, check_security_blacklist=True):
        """
        Install .cati package

        Args:
            pkg (BaseArchive): the package archive object
            index_updater_events (dict): events will be passed to `dotcati.ListUpdater.update_indexes()`
            installer_events (dict): The events
                - package_currently_install: gets the current installed version
                - package_new_installs: gets package archive
                - package_installed: will call after package installation
                - dep_and_conflict_error: will run when there is depends or conflict error
                - arch_error: will run when package arch is not sync with sys arch
            is_manual (bool): installed package as manual or not (default is True means manual)
            run_scripts (bool): run package install scripts or not (default is True)
            target_path (str): where is the target path for installed files (will pass to `self.copy_files()`)
            keep_conffiles (bool): stil keep config files if changed (default is True)
            check_security_blacklist (bool): check package is in security blacklist or not
        """

        self.conffiles = pkg.get_conffiles()
        self.pkg = pkg
        self.keep_conffiles = keep_conffiles
        self.uncopied_conffiles = {}

        # check package is in security blacklist
        if check_security_blacklist:
            self.check_security_blacklist(pkg)

        # check package architecture
        if not pkg.data['arch'] in SysArch.allowed_archs():
            return installer_events['arch_error'](pkg)

        # add package data to lists
        self.add_package_to_lists(pkg, index_updater_events)

        # check package dependencies and conflicts
        try:
            self.check_dep_and_conf(pkg)
        except DependencyError as ex:
            return installer_events['dep_and_conflict_error'](pkg, ex)
        except ConflictError as ex:
            return installer_events['dep_and_conflict_error'](pkg, ex)

        # load old conffiles
        self.old_conffiles = []
        try:
            f = open(Env.installed_lists('/' + pkg.data['name'] + '/conffiles'), 'r')
            content = f.read()
            f.close()
            tmp = content.strip().split('\n')
            self.old_conffiles = [item.strip().split('@') for item in tmp]
        except:
            pass

        # extract package in a temp place
        temp_dir = Temp.make_dir()
        os.rmdir(temp_dir)
        try:
            pkg.extractall(temp_dir)
        except IsADirectoryError:
            pass
        self.extracted_package_dir = temp_dir

        # install package
        if Pkg.is_installed(pkg.data['name']):
            installer_events['package_currently_installed'](pkg, Pkg.installed_version(pkg.data['name']))
        else:
            installer_events['package_new_installs'](pkg)

        if run_scripts:
            self.run_script('ins-before')

        copied_files = self.copy_files(pkg, installer_events['directory_not_empty'], target_path)

        # set install configuration
        if not os.path.isdir(Env.installed_lists('/' + pkg.data['name'])):
            os.mkdir(Env.installed_lists('/' + pkg.data['name']))
        f_ver = open(Env.installed_lists('/' + pkg.data['name'] + '/ver'), 'w')
        f_ver.write(pkg.data['version']) # write installed version
        f_ver.close()

        # write copied files list
        f_files = open(Env.installed_lists('/' + pkg.data['name'] + '/files'), 'w')
        copied_files_str = ''
        for copied_file in copied_files:
            copied_files_str += copied_file + '\n'
        f_files.write(copied_files_str.strip()) # write copied files
        f_files.close()

        # write conffiles list
        f_conffiles = open(Env.installed_lists('/' + pkg.data['name'] + '/conffiles'), 'w')
        copied_conffiles_str = ''
        for copied_conffile in copied_files:
            if copied_conffile.split(':')[0] == 'cf':
                try:
                    conffile_hash = self.uncopied_conffiles[copied_conffile.split(':', 1)[-1]]
                except:
                    conffile_hash = calc_file_sha256(Env.base_path(copied_conffile.split(':', 1)[-1]))
                copied_conffiles_str += conffile_hash + '@' + copied_conffile.split(':', 1)[-1] + '\n'
        f_conffiles.write(copied_conffiles_str.strip()) # write copied conffiles
        f_conffiles.close()

        # copy `any` script
        if os.path.isfile(self.extracted_package_dir + '/scripts/any'):
            os.system('cp "' + self.extracted_package_dir + '/scripts/any' + '" "' + Env.any_scripts('/' + pkg.data['name']) + '"')

        # save static files list
        static_files_list = pkg.get_static_files()
        f_static_files = open(Env.installed_lists('/' + pkg.data['name'] + '/staticfiles'), 'w')
        static_files_str = ''
        for copied_file in copied_files:
            copied_file_path = copied_file.split(':', 1)[1]
            if copied_file_path in static_files_list:
                if os.path.isfile(Env.base_path('/' + copied_file_path)):
                    # calculate file sha256 sum
                    copied_file_sha256 = calc_file_sha256(Env.base_path('/' + copied_file_path))
                    # add file to list
                    static_files_str += copied_file_sha256 + '@' + copied_file_path + '\n'
        f_static_files.write(static_files_str.strip()) # write copied files
        f_static_files.close()

        f_installed_at = open(Env.installed_lists('/' + pkg.data['name'] + '/installed_at'), 'w')
        f_installed_at.write(str(time.time())) # write time (installed at)
        f_installed_at.close()

        if is_manual:
            f_manual = open(Env.installed_lists('/' + pkg.data['name'] + '/manual'), 'w')
            f_manual.write('')
            f_manual.close()

        if run_scripts:
            self.run_script('ins-after')

        # copy remove scripts
        if os.path.isfile(self.extracted_package_dir + '/scripts/rm-before'):
            os.system(
                'cp "' + self.extracted_package_dir + '/scripts/rm-before' + '" "' + Env.installed_lists('/' + pkg.data['name'] + '/rm-before') + '"'
            )
        if os.path.isfile(self.extracted_package_dir + '/scripts/rm-after'):
            os.system(
                'cp "' + self.extracted_package_dir + '/scripts/rm-after' + '" "' + Env.installed_lists('/' + pkg.data['name'] + '/rm-after') + '"'
            )

        # pop package from state
        BaseTransaction.pop_state()

        # call package installed event
        installer_events['package_installed'](pkg)

    def add_package_to_lists(self, pkg: Pkg, index_updater_events: dict):
        """
        Adds the package information to database
        
        Args:
            pkg (Pkg): the package
            index_updater_events (dict): events for index updater
        """
        if not os.path.isdir(Env.packages_lists('/' + pkg.data['name'])):
            os.mkdir(Env.packages_lists('/' + pkg.data['name']))
        lists_path = Env.packages_lists('/' + pkg.data['name'] + '/' + pkg.data['version'] + '-' + pkg.data['arch'])
        try:
            lists_f = open(lists_path, 'r')
            old_repo = json.loads(lists_f.read())['repo']
            lists_f.close()
        except:
            old_repo = 'Local'
        try:
            lists_f = open(lists_path, 'r')
            old_file_path = json.loads(lists_f.read())['file_path']
            lists_f.close()
        except:
            old_file_path = False
        try:
            lists_f = open(lists_path, 'r')
            old_file_sha256 = json.loads(lists_f.read())['file_sha256']
            lists_f.close()
        except:
            old_file_sha256 = False
        try:
            lists_f = open(lists_path, 'r')
            old_file_md5 = json.loads(lists_f.read())['file_md5']
            lists_f.close()
        except:
            old_file_md5 = False
        lists_f = open(lists_path, 'w')
        pkg.data['repo'] = old_repo
        if old_file_path != False:
            pkg.data['file_path'] = old_file_path
        tmp_pkg_data = pkg.data
        if old_file_md5:
            tmp_pkg_data['file_md5'] = old_file_md5
        if old_file_sha256:
            tmp_pkg_data['file_sha256'] = old_file_sha256
        tmp_pkg_data['files'] = ['/' + member[6:] for member in pkg.members() if member[:6] == 'files/']
        lists_f.write(json.dumps(tmp_pkg_data))
        lists_f.close()
        ListUpdater.update_indexes(index_updater_events)
        ListUpdater.index_reverse_depends_and_conflicts(pkg)
