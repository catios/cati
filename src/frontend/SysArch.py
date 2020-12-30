#
# SysArch.py
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

""" Handle system architecture """

import os
from . import Env

is_testing = False
"""
in testing environment,
default architecture is `i386`, not real host arch.
"""

def sys_arch() -> str:
    """ Returns system architecture """
    if is_testing:
        return 'i386'
    else:
        arch = os.uname().machine
        if arch == 'i686':
            arch = 'i386'
        return arch

def allowed_archs() -> list:
    """
    Returns list of allowed architectures to install on the system

    The default archs are `all` and system architecture. also more archs
    will be loaded from /etc/cati/allowed-architectures.list

    Returns:
        list: list of allowed archs like ['all', 'amd64', '...']
    """
    # set default archs
    archs = ['all', sys_arch()]

    # load added archs
    f = open(Env.allowed_archs(), 'r')
    content = f.read()
    f.close()

    content = content.strip().split('\n')
    content = [line.strip() for line in content if line.strip() != '']
    archs = [*archs, *content]

    # remove repeated items from list
    archs = list(dict.fromkeys(archs))

    return archs
