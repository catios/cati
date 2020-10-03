#
# PkgCommand.py
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


''' Pkg command to work with .cati archives '''

from cmdline.BaseCommand import BaseCommand
from cmdline import pr
from cmdline import tcolor
from dotcati.Builder import Builder
from dotcati.Installer import Installer
from dotcati.exceptions.InvalidPackageDirException import InvalidPackageDirException
from dotcati.exceptions.InvalidPackageFileException import InvalidPackageFileException
from dotcati.ArchiveModel import ArchiveModel
from frontend.RootRequired import require_root_permission
from package.exceptions.CannotReadFileException import CannotReadFileException

class PkgCommand(BaseCommand):
    def help(self):
        '''
        work with .cati packages
        
        Subcommands:
        - build:      build .cati package from directory(s)
        - show:       show content of .cati package(s)
        - install:    install a .cati package on system
        '''
        pass

    def define(self) -> dict:
        ''' Define and config this command '''
        return {
            'name': 'pkg',
            'options': {
                '--output': [False , True],
                '-o': [False , True],
                '--files': [False , False],
                '-f': [False , False],
            },
            'max_args_count': None,
            'min_args_count': None,
        }

    def sub_build(self):
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
                output_package = builder.build(self.arguments[i] , output)

                pr.p(tcolor.OKGREEN + 'Package ' + self.arguments[i] + ' created successfuly in ' + output_package + tcolor.ENDC)
            except FileNotFoundError as ex:
                self.message('directory "' + self.arguments[i] + '" not found' + tcolor.ENDC , before=tcolor.FAIL)
            except InvalidPackageDirException as ex:
                self.message('cannot build "' + self.arguments[i] + '": ' + str(ex) + tcolor.ENDC , before=tcolor.FAIL)

            i += 1

    def show_once(self , pkg: ArchiveModel):
        # TODO : print more fields
        output = ''
        output += 'Name: ' + pkg.data['name'] + '\n'
        output += 'Version: ' + pkg.data['version'] + '\n'
        output += 'Arch: ' + pkg.data['arch']
        pr.p(output)
        if self.has_option('--files') or self.has_option('-f'):
            pr.p('Files:')
            pkg.tar.list()
        if len(self.arguments) > 2:
            pr.p('='*50)

    def sub_show(self):
        if len(self.arguments) <= 1:
            self.message('argument package file(s) required')
            return 1
        
        i = 1
        while i < len(self.arguments):
            try:
                pkg = ArchiveModel(self.arguments[i] , 'r')
                pkg.read()
                self.show_once(pkg)
                pkg.close()
            except FileNotFoundError as ex:
                self.message('file "' + self.arguments[i] + '" not found' + tcolor.ENDC , before=tcolor.FAIL)
            except:
                self.message('cannot open "' + self.arguments[i] + '": file is corrupt' + tcolor.ENDC , before=tcolor.FAIL)

            i += 1

    def cannot_read_file_event(self , path):
        self.message('error while reading file "' + path + '". ignored...' + tcolor.ENDC , before=tcolor.FAIL)
    
    def invalid_json_data_event(self , path):
        self.message('invalid json data in "' + path + '". ignored...' + tcolor.ENDC , before=tcolor.FAIL)

    def package_currently_installed_event(self , package: ArchiveModel , current_version: str):
        pr.p('Installing ' + package.data['name'] + ':' + package.data['version'] + ' over ' + current_version)

    def package_new_installs_event(self , package: ArchiveModel):
        pr.p('Installing ' + package.data['name'] + ':' + package.data['version'])

    def install_once(self , pkg: ArchiveModel):
        installer = Installer()

        try:
            installer.install(pkg , {
                'cannot_read_file': self.cannot_read_file_event,
                'invalid_json_data': self.invalid_json_data_event,
            },
            {
                'package_currently_installed': self.package_currently_installed_event,
                'package_new_installs': self.package_new_installs_event,
            })
        except CannotReadFileException as ex:
            self.message(tcolor.FAIL + str(ex) , True , before=tcolor.ENDC)
        except:
            raise

    def sub_install(self):
        if len(self.arguments) <= 1:
            self.message('argument package file(s) required')
            return 1

        require_root_permission()

        i = 1
        while i < len(self.arguments):
            try:
                pkg = ArchiveModel(self.arguments[i] , 'r')
                pkg.read()
                self.install_once(pkg)
                pkg.close()
            except FileNotFoundError as ex:
                self.message('file "' + self.arguments[i] + '" not found' + tcolor.ENDC , before=tcolor.FAIL)
            except:
                self.message('cannot open "' + self.arguments[i] + '": file is corrupt' + tcolor.ENDC , before=tcolor.FAIL)

            i += 1

    def run(self):
        ''' Run command '''

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
            self.message('unknow subcommand "' + self.arguments[0] + '"' , True)
            return 1
