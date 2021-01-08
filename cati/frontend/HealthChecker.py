#
# HealthChecker.py
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

""" Checks cati installation health and repair """

import os
from . import Env

def repair_once_file(filepath: str, events: dict):
    """
    Repairs once file

    Args:
        filepath (str): the filepath to repair
        events (dict):
            - faild_to_repair
    """
    try:
        f = open(Env.base_path('/' + filepath).replace('//', '/'), 'w')
        f.write('')
        f.close()
    except:
        events['failed_to_repair']('/' + filepath, 'file')

def repair_once_dir(dirpath: str, events: dict):
    """
    Repairs once dir

    Args:
        dirpath (str): the dirpath to repair
        events (dict):
            - faild_to_repair
    """
    try:
        os.mkdir(Env.base_path('/' + dirpath))
    except:
        events['failed_to_repair']('/' + dirpath, 'dir')

def check(events: dict):
    """
    Check all of needed files and dirs for cati installation

    Args:
        events:
            - failed_to_repair: will run when cati installation is corrupt and user has not root permission
            to repair it and passes filepath and type of that to function
    """

    required_files = [
        '/var/lib/cati/state.f',
        '/var/lib/cati/unremoved-conffiles.list',
        '/etc/cati/repos.list',
        '/etc/cati/allowed-architectures.list',
    ]

    required_dirs = [
        '/var',
        '/var/lib',
        '/var/lib/cati',
        '/var/lib/cati/lists',
        '/var/lib/cati/installed',
        '/var/lib/cati/security-blacklist',
        '/var/lib/cati/any-scripts',
        '/var/cache',
        '/var/cache/cati',
        '/var/cache/cati/archives',
        '/etc',
        '/etc/cati',
        '/etc/cati/repos.list.d',
    ]

    for d in required_dirs:
        if not os.path.isdir(Env.base_path('/' + d)):
            repair_once_dir(d, events)

    for f in required_files:
        if not os.path.isfile(Env.base_path('/' + f)):
            repair_once_file(f, events)
