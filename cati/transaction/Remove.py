#
# Remove.py
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

""" Remove transaction """

import os
import shutil
from cati.transaction.BaseTransaction import BaseTransaction
from cati.dotcati.Pkg import Pkg
from cati.frontend import Env

class Remove(BaseTransaction):
    """ Remove transaction """
    @staticmethod
    def add_to_unremoved_conffiles(pkg: Pkg, filepath: str):
        """ Adds filepath to list of unremoved conffiles """
        f = open(Env.unremoved_conffiles(), 'r')
        filelist = f.read().strip().split('\n')
        f.close()

        # add item to list
        if not filepath in filelist:
            filelist.append(filepath)

        # generate new content of unremoved_conffiles file
        new_content = ''
        for item in filelist:
            new_content += item + '\n'

        # write new content to file
        f = open(Env.unremoved_conffiles(), 'w')
        f.write(new_content)
        f.close()

    @staticmethod
    def run(pkg: Pkg, events: dict, remove_conffiles=False, run_scripts=True):
        """ Remove pkg """
        events['removing_package'](pkg)

        # run rm-before script
        if run_scripts:
            if os.path.isfile(Env.installed_lists('/' + pkg.data['name'] + '/rm-before')):
                os.system('chmod +x "' + Env.installed_lists('/' + pkg.data['name'] + '/rm-before') + '"')
                with_conffiles_arg = 'without-conffiles'
                if remove_conffiles:
                    with_conffiles_arg = 'with-conffiles'
                os.system(Env.installed_lists('/' + pkg.data['name'] + '/rm-before') + ' ' + with_conffiles_arg)

        # remove package
        installed_files = open(Env.installed_lists('/' + pkg.data['name'] + '/files'), 'r').read()
        installed_files = installed_files.strip().split('\n')
        for f in list(reversed(installed_files)):
            if f != '':
                f_type = f.strip().split(':', 1)[0]
                f_path = f.strip().split(':', 1)[1]
                if f_type == 'f':
                    if os.path.isfile(Env.base_path(f_path)):
                        os.remove(Env.base_path(f_path))
                elif f_type == 'd':
                    try:
                        os.rmdir(Env.base_path(f_path))
                    except:
                        events['dir_is_not_empty'](pkg, f)
                elif f_type == 'cf':
                    if remove_conffiles:
                        if os.path.isfile(Env.base_path(f_path)):
                            os.remove(Env.base_path(f_path))
                    else:
                        Remove.add_to_unremoved_conffiles(pkg, f_path)
                elif f_type == 'cd':
                    if remove_conffiles:
                        try:
                            os.rmdir(Env.base_path(f_path))
                        except:
                            events['dir_is_not_empty'](pkg, f)
                    else:
                        Remove.add_to_unremoved_conffiles(pkg, f_path)

        # run rm-after script
        if run_scripts:
            if os.path.isfile(Env.installed_lists('/' + pkg.data['name'] + '/rm-after')):
                with_conffiles_arg = 'without-conffiles'
                if remove_conffiles:
                    with_conffiles_arg = 'with-conffiles'
                os.system('chmod +x "' + Env.installed_lists('/' + pkg.data['name'] + '/rm-after') + '"')
                os.system(Env.installed_lists('/' + pkg.data['name'] + '/rm-after') + ' ' + with_conffiles_arg)

        # remove installation config
        shutil.rmtree(Env.installed_lists('/' + pkg.data['name']))

        # remove any script
        if os.path.isfile(Env.any_scripts('/' + pkg.data['name'])):
            os.remove(Env.any_scripts('/' + pkg.data['name']))

        events['package_remove_finished'](pkg)
