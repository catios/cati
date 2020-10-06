#
# RootRequired.py
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

''' A tool to check program permission and if it haven't root permission, die the program '''

import os, sys
from cmdline import pr
from cmdline import ansi

def require_root_permission(is_cli=True , die_action=None):
    '''
    If `is_cli` argument is True, when user have not root permission,
    error will print on terminal. but if is False,
    the `die_action` will run as a function
    '''

    if os.getuid() != 0:
        if is_cli:
            pr.e(ansi.red + sys.argv[0] + ': permission is denied' + ansi.reset)
            pr.exit(1)
        else:
            die_action()
