#
# Temp.py
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

""" Handle temp files """

import random
import os
import shutil

created_temp_dirs = []
created_temp_files = []

def make_dir() -> str:
    """ Makes a temp directory and returns path of that directory """
    global created_temp_dirs
    path = '/tmp/' + 'cati-temp-' + str(random.random())

    if os.path.exists(path):
        return make_dir()

    os.mkdir(path)
    created_temp_dirs.append(path)
    return path

def make_file() -> str:
    """ Makes a temp file and returns path of that file """
    global created_temp_files
    path = '/tmp/' + 'cati-temp-' + str(random.random())

    if os.path.exists(path):
        return make_file()

    f = open(path, 'w')
    f.write('')
    f.close()
    created_temp_dirs.append(path)
    return path

def clean():
    """ Clear all of created temp files by program """
    global created_temp_dirs, created_temp_files

    for f in created_temp_files:
        if os.path.isfile(f):
            try:
                os.remove(f)
            except:
                pass

    for d in created_temp_dirs:
        if os.path.isdir(d):
            try:
                shutil.rmtree(d)
            except:
                pass

    created_temp_dirs = []
    created_temp_files = []
