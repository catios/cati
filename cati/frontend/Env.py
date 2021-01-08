#
# Env.py
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

"""
Handle environment file paths.

in cati, we do not write config, database and... file paths directly in everywhere.
we get that paths from this module.
also testing system changes base environment path in `base_path_dir` variable
to isolate program environemnt while running tests
"""

base_path_dir = ''
"""
str: base path of the cati files environment.
(will get another path in testing environment to isolate testing environment with real environment)
"""

def base_path(path=''):
    """ Returns environment base path """
    return base_path_dir + path

def packages_lists(path=''):
    """ Packages list directory """
    return base_path('/var/lib/cati/lists' + path)

def installed_lists(path=''):
    """ Installed packages list directory """
    return base_path('/var/lib/cati/installed' + path)

def state_file():
    """ State file (read state system documentation) """
    return base_path('/var/lib/cati/state.f')

def unremoved_conffiles():
    """ Unremoved conffiles list filepath """
    return base_path('/var/lib/cati/unremoved-conffiles.list')

def security_blacklist(path=''):
    """ Security blacklist directory """
    return base_path('/var/lib/cati/security-blacklist' + path)

def any_scripts(path=''):
    """ Any scripts directory """
    return base_path('/var/lib/cati/any-scripts' + path)

def repos_config():
    return base_path('/etc/cati/repos.list')

def repos_config_dir(path=''):
    return base_path('/etc/cati/repos.list.d' + path)

def cache_dir(path=''):
    return base_path('/var/cache/cati' + path)

def allowed_archs():
    return base_path('/etc/cati/allowed-architectures.list')
