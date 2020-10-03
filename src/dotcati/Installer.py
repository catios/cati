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

import os, json, time
from dotcati.ArchiveModel import ArchiveModel
from frontend import Env
from dotcati import ListUpdater
from package.Pkg import Pkg

class Installer:
    ''' Dotcati package installer '''        
    def install(self , pkg: ArchiveModel , index_updater_events: dict , installer_events: dict):
        '''
        Install .cati package

        installer_events:
        - package_currently_install: gets a current installed version
        - package_new_installs: gets package archive
        '''

        # add package data to lists
        if not os.path.isdir(Env.packages_lists('/' + pkg.data['name'])):
            os.mkdir(Env.packages_lists('/' + pkg.data['name']))
        
        lists_path = Env.packages_lists('/' + pkg.data['name'] + '/' + pkg.data['version'] + '-' + pkg.data['arch'])

        try:
            lists_f = open(lists_path , 'r')
            old_repo = json.loads(lists_f.read())['repo']
            lists_f.close()
        except:
            old_repo = 'Local'
            pass

        lists_f = open(lists_path , 'w')
        pkg.data['repo'] = old_repo
        lists_f.write(json.dumps(pkg.data))
        lists_f.close()

        ListUpdater.update_indexes(index_updater_events)

        # install package
        if Pkg.is_installed(pkg.data['name']):
            installer_events['package_currently_installed'](pkg , Pkg.installed_version(pkg.data['name']))
        else:
            installer_events['package_new_installs'](pkg)

        # TODO : copy package files on system

        # set install configuration
        if not os.path.isdir(Env.installed_lists('/' + pkg.data['name'])):
            os.mkdir(Env.installed_lists('/' + pkg.data['name']))
        f_ver = open(Env.installed_lists('/' + pkg.data['name'] + '/ver') , 'w')
        f_ver.write(pkg.data['version'])
        f_ver.close()

        f_files = open(Env.installed_lists('/' + pkg.data['name'] + '/files') , 'w')
        f_files.write('')
        f_files.close()

        f_installed_at = open(Env.installed_lists('/' + pkg.data['name'] + '/installed_at') , 'w')
        f_installed_at.write(str(time.time()))
        f_installed_at.close()
