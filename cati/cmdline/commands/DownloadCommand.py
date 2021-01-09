#
# DownloadCommand.py
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

""" Download command """

import os
import shutil
from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.cmdline.components import DownloadProgress
from cati.dotcati.Pkg import Pkg

class DownloadCommand(BaseCommand):
    """ Download command """
    def help(self):
        """
        download packages

        Usage: cati download pkg1 pkg1 ... [options]
        ...... cati download pkg=<version> pkg2=<version> pkg3 ... [options]
        ...... cati download pkg=<version>=<arch> ... [options]

        Options:
        --output=[output file path]: set file download path
        -q|--quiet: quiet output
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'download',
            'options': {
                '-q': [False, False],
                '--quiet': [False, False],
                '--output': [False, True],
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def download_once(self, pkg, output=None):
        """ Download once package """

        try:
            file_path = pkg.data['file_path']
        except:
            self.message('package "' + pkg.data['name'] + '" is local and cannot be downloaded' + ansi.reset, is_error=True, before=ansi.red)
            return False
        if not self.is_quiet():
            pr.p('Downloading ' + pkg.data['name'] + ':' + pkg.data['version'] + ':' + pkg.data['arch'] + '...')

        if output == None:
            output = file_path.split('/')[-1]

        if file_path[:7] == 'http://' or file_path[:8] == 'https://':
            i = 0
            while i < 5:
                res = DownloadProgress.download(file_path, output)
                if res == True:
                    break
                else:
                    pr.e(ansi.red + str(res) + ansi.reset)
                i += 1
            if i == 5:
                return False
        else:
            if not os.path.isfile(file_path):
                return False
            shutil.copy(file_path, output)

        return True

    def run(self):
        """ Run command """

        if not self.is_quiet():
            pr.p('Loading packages list...')
            pr.p('========================')

        loaded_packages = []

        for argument in self.arguments:
            arg_parts = argument.split('=')
            if len(arg_parts) == 1:
                # load last version as default
                pkg = Pkg.load_last(argument)
            elif len(arg_parts) == 2:
                # load specify version
                pkg = Pkg.load_version(arg_parts[0], arg_parts[1])
                if pkg == 1:
                    pkg = False
                elif pkg == 2:
                    self.message('package "' + arg_parts[0] + '" has not version "' + arg_parts[1] + '"' + ansi.reset, before=ansi.red)
                    continue
            else:
                # load specify version and specify arch
                pkg = Pkg.load_version(arg_parts[0], arg_parts[1], arg_parts[2])
                if pkg == 1:
                    pkg = False
                elif pkg == 2:
                    self.message('package "' + arg_parts[0] + '" has not version or arch "' + arg_parts[1] + ':' + arg_parts[2] + '"' + ansi.reset, before=ansi.red)
                    continue
            if pkg:
                loaded_packages.append(pkg)
            else:
                self.message('unknow package "' + argument + '"' + ansi.reset, before=ansi.red)

        if not loaded_packages:
            return 1

        # download loaded packages
        is_any_success = False
        output_path = self.option_value('--output')
        for pkg in loaded_packages:
            if len(loaded_packages) > 1:
                tmp = self.download_once(pkg)
            else:
                tmp = self.download_once(pkg, output_path)
            if tmp:
                is_any_success = True

        if not is_any_success:
            return 1
