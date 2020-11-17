#
# SysArch.py
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

""" Handle system architecture """

import os

is_testing = False
"""
in testing environment,
default architecture is `i386`, not real host arch.
"""

def sys_arch():
    """ Returns system architecture """
    if is_testing:
        return 'i386'
    else:
        arch = os.uname().machine
        if arch == 'i686':
            arch = 'i386'
        return arch
