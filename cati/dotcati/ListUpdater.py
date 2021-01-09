#
# ListUpdater.py
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

""" Database Packages list updater """

import os
import json
from cati.frontend.RootRequired import require_root_permission
from cati.frontend import Env
from .Pkg import Pkg

def update_indexes(events: dict):
    """
    This function loads available versions of a package and index them in index file
    and do this action for all of packages in lists.

    Args:
        events: (dict) the `events` argument should be a dictonary from functions. this will use to handle errors
                for example if some thing went wrong, the spesific function in events
                will run.
                events:
                - cannot_read_file: if in this process, an error happened while reading a file, this will run with file path arg
                - invalid_json_data: if json content of a file is curropt, this will run with file path and content args
    """

    require_root_permission()

    for pkg in os.listdir(Env.packages_lists()):
        pkg_index = {}
        if os.path.isdir(Env.packages_lists('/' + pkg)):
            for version in os.listdir(Env.packages_lists('/' + pkg)):
                if version not in ['index', 'reverse_depends', 'reverse_conflicts']:
                    if os.path.isfile(Env.packages_lists('/' + pkg + '/' + version)):
                        content = None
                        try:
                            f = open(Env.packages_lists('/' + pkg + '/' + version), 'r')
                            content = f.read()
                        except:
                            events['cannot_read_file'](Env.packages_lists('/' + pkg + '/' + version))

                        if content != None:
                            try:
                                content_json = json.loads(content)
                                try:
                                    tmp = pkg_index[content_json['arch']]
                                    del tmp
                                except:
                                    pkg_index[content_json['arch']] = []
                                pkg_index[content_json['arch']].append(content_json['version'])
                            except:
                                events['invalid_json_data'](Env.packages_lists('/' + pkg + '/' + version), content)
        # write generated index to index file
        f_index = open(Env.packages_lists('/' + pkg + '/index'), 'w')
        f_index.write(json.dumps(pkg_index))
        f_index.close()

def index_reverse_depends_and_conflicts(pkg: Pkg):
    """
    Packages have `depends` and `conflicts`
    But also they have `Reverse` depends and conflicts
    Reverse d/c should be indexed because loading them real time is so big process
    We index them in a place, and when a package is added/changed, this function should be called

    Args:
        pkg (Pkg): changed/added package (reverse c/d will be set for that packages this package is related to them)
    """
    # load the packages
    depend_pkgs = []
    conflict_pkgs = []
    for depend in pkg.get_depends():
        query_parts = Pkg.check_state(depend, only_parse=True)
        for depth1 in query_parts:
            for depth2 in depth1:
                depend_pkgs.append(depth2[0])
    for conflict in pkg.get_conflicts():
        query_parts = Pkg.check_state(conflict, only_parse=True)
        for depth1 in query_parts:
            for depth2 in depth1:
                conflict_pkgs.append(depth2[0])

    # set reverse depends/conflicts for found packages
    for p in depend_pkgs:
        f_path = Env.packages_lists('/' + p + '/reverse_depends')
        current_list = None
        try:
            if not os.path.isdir(Env.packages_lists('/' + p)):
                os.mkdir(Env.packages_lists('/' + p))
            if not os.path.isfile(f_path):
                current_list = []
            else:
                f = open(f_path, 'r')
                current_list = [item.strip() for item in f.read().strip().split('\n') if item.strip() != '']
                f.close()
            if not pkg.data['name'] in current_list:
                current_list.append(pkg.data['name'])
            # write new list
            new_list_str = ''
            for item in current_list:
                new_list_str += item + '\n'
            new_list_str = new_list_str.strip()
            f = open(f_path, 'w')
            f.write(new_list_str)
            f.close()
        except:
            pass
    for p in conflict_pkgs:
        f_path = Env.packages_lists('/' + p + '/reverse_conflicts')
        current_list = None
        try:
            if not os.path.isdir(Env.packages_lists('/' + p)):
                os.mkdir(Env.packages_lists('/' + p))
            if not os.path.isfile(f_path):
                current_list = []
            else:
                f = open(f_path, 'r')
                current_list = [item.strip() for item in f.read().strip().split('\n') if item.strip() != '']
                f.close()
            if not pkg.data['name'] in current_list:
                current_list.append(pkg.data['name'])
            # write new list
            new_list_str = ''
            for item in current_list:
                new_list_str += item + '\n'
            new_list_str = new_list_str.strip()
            f = open(f_path, 'w')
            f.write(new_list_str)
            f.close()
        except:
            pass
