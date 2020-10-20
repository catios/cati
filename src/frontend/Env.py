#
# Env.py
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

''' Handle environment file paths '''

base_path_dir = ''

def base_path(path=''):
    ''' Returns environment base path '''
    return base_path_dir + path

def packages_lists(path=''):
    ''' Packages list directory '''
    return base_path('/var/lib/cati/lists' + path)

def installed_lists(path=''):
    ''' Installed packages list directory '''
    return base_path('/var/lib/cati/installed' + path)
