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

import os, json
from dotcati.ArchiveModel import ArchiveModel
from frontend import Env
from dotcati import ListUpdater

class Installer:
    ''' Dotcati package installer '''        
    def install(self , pkg: ArchiveModel , index_updater_events: dict):
        ''' Install .cati package '''

        # add package data to lists
        if not os.path.isdir(Env.packages_lists('/' + pkg.data['name'])):
            os.mkdir(Env.packages_lists('/' + pkg.data['name']))
        
        lists_path = Env.packages_lists('/' + pkg.data['name'] + '/' + pkg.data['version'] + '-' + pkg.data['arch'])
        lists_f = open(lists_path , 'w')
        lists_f.write(json.dumps(pkg.data))
        lists_f.close()

        ListUpdater.update_indexes(index_updater_events)


