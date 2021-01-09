#
# PkgCommand.py
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

""" Pkg command to work with .cati archives """

import os
from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.dotcati.Builder import Builder
from cati.dotcati.Installer import Installer
from cati.dotcati.exceptions import InvalidPackageDirException, InvalidPackageFileException, DependencyError, ConflictError, PackageScriptError, PackageIsInSecurityBlacklist, FileConflictError, CannotReadFileException
from cati.dotcati.ArchiveModel import archive_factory, BaseArchive
from cati.frontend.RootRequired import require_root_permission
from cati.frontend import Env
from cati.cmdline.components import PackageShower, StateContentShower
from cati.transaction.BaseTransaction import BaseTransaction

class PkgCommand(BaseCommand):
    """ Pkg command to work with .cati archives """
    def help(self):
        """
        work with .cati packages

        Usage: cati pkg [subcommand] [args] [options]

        Subcommands:
        - build:      build .cati package from directory(s)
        - show:       show content of .cati package(s). options: --files: show package files
        - install:    install a .cati package on system

        Options:
        - install subcommand:
        * --without-scripts: do not run package scripts in installation process
        * --target=[files-install-location-prefix-path]: set files installation prefix
        * --keep-conffiles: don't overwrite new version of config files
        * --force|-f: force install that packages are blocked in securiy blacklist
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'pkg',
            'options': {
                '--quiet': [False, False],
                '-q': [False, False],
                '--output': [False, True],
                '-o': [False, True],
                '--files': [False, False],
                '-f': [False, False],
                '--auto': [False, False],
                '--without-scripts': [False, False],
                '--target': [False, True],
                '--dont-ignore-state': [False, False],
                '--keep-conffiles': [False, False],
                '--force': [False, False],
                '-f': [False, False],
            },
            'max_args_count': None,
            'min_args_count': None,
        }

    def sub_build(self):
        """ build subcommand (cati pkg build) """
        if len(self.arguments) <= 1:
            self.message('argument package directory(s) required')
            return 1

        i = 1
        while i < len(self.arguments):
            try:
                output = self.option_value('--output')
                if output == None:
                    output = self.option_value('-o')
                builder = Builder()
                output_package = builder.build(self.arguments[i], output)
                if not self.is_quiet():
                    pr.p(ansi.green + 'Package ' + self.arguments[i] + ' created successfuly in ' + output_package + ansi.reset)
            except FileNotFoundError as ex:
                self.message('directory "' + self.arguments[i] + '" not found' + ansi.reset, before=ansi.red)
                return 1
            except InvalidPackageDirException as ex:
                self.message('cannot build "' + self.arguments[i] + '": ' + str(ex) + ansi.reset, before=ansi.red)
                return 1

            i += 1

    def show_once(self, pkg: BaseArchive):
        """
        shows once package (called from `show` subcommand function)
        gives package data to cli package sohwer component to show package info
        """
        PackageShower.show(pkg.data)
        if self.has_option('--files') or self.has_option('-f'):
            pr.p('Files:')
            pkg.tar.list()
        if len(self.arguments) > 2:
            pr.p('='*50)

    def sub_show(self):
        """ show subcommand (cati pkg show) """
        if len(self.arguments) <= 1:
            self.message('argument package file(s) required')
            return 1

        i = 1
        while i < len(self.arguments):
            try:
                pkg = archive_factory(self.arguments[i], 'r')
                pkg.read()
                self.show_once(pkg)
                pkg.close()
            except FileNotFoundError as ex:
                self.message('file "' + self.arguments[i] + '" not found' + ansi.reset, before=ansi.red)
            except:
                self.message('cannot open "' + self.arguments[i] + '": file is corrupt' + ansi.reset, before=ansi.red)

            i += 1

    def cannot_read_file_event(self, path):
        """
        index updater cannot_read_file event
        will pass to installer and installer passes this to index updater
        """
        self.message('error while reading file "' + path + '". ignored...' + ansi.reset, before=ansi.red)

    def invalid_json_data_event(self, path, content):
        """
        index updater invalid_json_data event
        will pass to installer and installer passes this to index updater
        """
        self.message('invalid json data in "' + path + '". ignored...' + ansi.reset, before=ansi.red)

    def package_currently_installed_event(self, package: BaseArchive, current_version: str):
        """
        installer package_currently_installed event
        will run when package already installed
        gets package and current installed version
        """
        pr.p('Installing ' + ansi.yellow + package.data['name'] + ':' + package.data['version'] + ansi.reset + ' (over ' + ansi.yellow + current_version + ansi.reset + ')...', end=' ')

    def package_new_installs_event(self, package: BaseArchive):
        """
        installer package_new_installs event
        will run when package will NEW installed
        """
        pr.p('Installing ' + ansi.yellow + package.data['name'] + ':' + package.data['version'] + ansi.reset + '...', end=' ')

    def package_installed_event(self, package: BaseArchive):
        """
        installer package_installed event
        will run when package installation finshed
        """
        pr.p(ansi.green + 'OK' + ansi.reset)

    def directory_not_empty_event(self, package: BaseArchive, dirpath: str):
        """
        installer directory_not_empty event
        will run when package old directory is not empty
        """
        pr.e(ansi.yellow + 'warning: directory "' + dirpath + '" is not empty and will not be deleted' + ansi.reset)

    def dep_and_conflict_error_event(self, pkg: BaseArchive, ex: Exception):
        """
        installer dep_and_conflict_error event
        will run when package has conflict/dependency error while installing it
        `ex` argument can be DependencyError or ConflictError
        """
        pr.e(
            ansi.red +\
            'Error while installing ' + pkg.data['name'] + ' (' + pkg.data['version'] + '):',
        )
        if isinstance(ex, DependencyError):
            pr.e('\tdependency error:')
        elif isinstance(ex, ConflictError):
            pr.e('\tconflict error:')
        pr.e('\t\t' + str(ex))
        pr.e(ansi.reset)

        return 1

    def arch_error_event(self, pkg: BaseArchive):
        """
        installer arch_error event
        will run when package architecture is not supported on the system
        for example while installing `amd64` package on `i386` system
        """
        pr.e(ansi.red + 'Architecture error while installing "' + pkg.data['name'] + '": your system does not support "' + pkg.data['arch'] + '" packages.' + ansi.reset)
        return 1

    def install_once(self, pkg: BaseArchive):
        """
        installs once package
        is called from install sub command
        """
        target_path = self.option_value('--target')
        if target_path == None:
            target_path = ''
        installer = Installer()

        try:
            out = installer.install(pkg,
                {
                    'cannot_read_file': self.cannot_read_file_event,
                    'invalid_json_data': self.invalid_json_data_event,
                },
                {
                    'package_currently_installed': self.package_currently_installed_event,
                    'package_new_installs': self.package_new_installs_event,
                    'package_installed': self.package_installed_event,
                    'directory_not_empty': self.directory_not_empty_event,
                    'dep_and_conflict_error': self.dep_and_conflict_error_event,
                    'arch_error': self.arch_error_event,
                },
                (not self.has_option('--auto')),
                run_scripts=(not self.has_option('--without-scripts')),
                target_path=str(target_path),
                keep_conffiles=self.has_option('--keep-conffiles'),
                check_security_blacklist=(not self.has_option('--force') and not self.has_option('-f'))
            )

            if type(out) == int:
                return out
        except PackageScriptError as ex:
            pr.e(ansi.red + 'cannot install "' + pkg.data['name'] + ':' + pkg.data['version'] + '": ' + str(ex) + ansi.reset)
            return 1
        except PackageIsInSecurityBlacklist as ex:
            pr.e(ansi.red + 'cannot install ' + pkg.data['name'] + ':' + pkg.data['version'] + ' because this is in security blacklist:')
            pr.e('  ' + ex.blacklist_item['title'] + ':')
            for l in ex.blacklist_item['description'].split('\n'):
                pr.e('\t' + l)
            pr.p(ansi.reset, end='')
            return 1
        except CannotReadFileException as ex:
            self.message(ansi.red + str(ex), True, before=ansi.reset)
            return 1
        except FileConflictError as ex:
            pr.e(ansi.red + '\nCannot install ' + pkg.data['name'] + ':' + pkg.data['version'] + ': File conflict error:')
            pr.e('    ' + str(ex))
            pr.p(ansi.reset, end='')
            return 1

    def start_run_any_script_event(self, package_name: str):
        """ will run when starting running an `any` script """
        pr.p('Processing scripts for ' + package_name + '...')

    def sub_install(self):
        """ install sub command (cati pkg install) """
        if len(self.arguments) <= 1:
            self.message('argument package file(s) required')
            return 1

        require_root_permission()

        # check transactions state before run new transactions
        pr.p('Checking transactions state...')
        state_list = BaseTransaction.state_list() # get list of undoned transactions
        if state_list:
            # the list is not empty
            StateContentShower.show(state_list)
            return 1

        packages_to_install = []
        i = 1
        while i < len(self.arguments):
            try:
                pkg = archive_factory(self.arguments[i], 'r')
                pkg.read()
                pkg.package_file_path = os.path.abspath(self.arguments[i])
                packages_to_install.append(pkg)
            except FileNotFoundError as ex:
                self.message('file "' + self.arguments[i] + '" not found' + ansi.reset, before=ansi.red)
                return 1
            except:
                self.message('cannot open "' + self.arguments[i] + '": file is corrupt' + ansi.reset, before=ansi.red)
                return 1

            i += 1

        # add packages to state
        state_f = open(Env.state_file(), 'w')
        tmp = ''
        for pkg in packages_to_install:
            tmp += ('install%' + pkg.data['name'] + '%' + pkg.data['version'] + '%' + pkg.data['arch'] + '%' + pkg.package_file_path + '\n')
        state_f.write(tmp)
        state_f.close()

        packages_to_install_names_and_versions = [pkg.data['name'] + '@' + pkg.data['version'] for pkg in packages_to_install]
        i = 0
        while i < len(packages_to_install):
            try:
                pkg = packages_to_install[i]
                tmp = self.install_once(pkg)
                if type(tmp) == int and tmp != 0:
                    if not self.has_option('--dont-ignore-state'):
                        BaseTransaction.finish_all_state()
                    return tmp
                pkg.close()
            except:
                if not self.has_option('--dont-ignore-state'):
                    BaseTransaction.finish_all_state()
                self.message('cannot install "' + packages_to_install[i].data['name'] + '"' + ansi.reset, before=ansi.red)
                return 1
            i += 1
        BaseTransaction.run_any_scripts(['install', packages_to_install_names_and_versions], events={
            'start_run_script': self.start_run_any_script_event,
        })
        BaseTransaction.finish_all_state()

    def run(self):
        """ Run command """

        if len(self.arguments) <= 0:
            pr.p(self.help_full())
            return 0
        
        if self.arguments[0] == 'build':
            return self.sub_build()
        elif self.arguments[0] == 'show':
            return self.sub_show()
        elif self.arguments[0] == 'install':
            return self.sub_install()
        else:
            self.message('unknow subcommand "' + self.arguments[0] + '"', True)
            return 1
