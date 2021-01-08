#
# Scanner.py
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

""" Scans an directory and create packages data files """

import os
import json
from cati.dotcati.ArchiveModel import archive_factory
from cati.helpers.hash import calc_file_sha256, calc_file_md5

def scan(directory: str):
    """
    Scans an directory and create packages data files
    
    Args:
        directory (str): the repository directory path
    """
    for item in os.listdir(directory):
        if os.path.isfile(directory + '/' + item):
            if item.split('.')[-1] in ['cati', 'deb', 'rpm']:
                try:
                    scan_once(directory + '/' + item)
                except:
                    pass
        else:
            scan(directory + '/' + item)

def scan_once(filepath: str):
    """
    Scan once package
    
    Args:
        filepath (str): the package filepath
    """
    pkg = archive_factory(filepath, 'r')
    pkg.read()
    data = pkg.data

    data['file_path'] = os.path.abspath(filepath)
    data['file_sha256'] = calc_file_sha256(filepath)
    data['file_md5'] = calc_file_md5(filepath)
    data['pkg_type'] = filepath.split('.')[-1]
    data['file_size'] = os.path.getsize(filepath)

    data_file = open(filepath + '.json', 'w')
    data_file.write(json.dumps(data))
    data_file.close()
    pkg.close()
