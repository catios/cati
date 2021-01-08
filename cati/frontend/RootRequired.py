#
# RootRequired.py
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

""" A tool to check program permission and if it haven't root permission, die the program """

import os
import sys
from cati.cmdline import pr, ansi
from . import Env

is_testing = False
"""
bool: this variable will be True in testing environment to disable root permission check
(root permission in not needed in testing environment)
"""

def require_root_permission(is_cli=True, die_action=None):
    """
    checks root premission.

    Args:
        is_cli (bool): if is True, when user have not root permission,
            error will print in terminal. but if is False,
            the `die_action` will run as a function.
            (will be disable in testing environment)
        die_action (callable): the function will be run when `is_cli` is False
    """

    # if program is in testing mode don't check permission
    if is_testing:
        return

    if os.getuid() == 0:
        return

    # check write and read access for needed files
    files_to_check = [
        Env.packages_lists(),
        Env.installed_lists(),
        Env.state_file(),
        Env.unremoved_conffiles(),
        Env.security_blacklist(),
        Env.any_scripts(),
        Env.repos_config(),
        Env.repos_config_dir(),
        Env.cache_dir(),
        Env.allowed_archs(),
    ]
    for f in files_to_check:
        if not os.access(f, os.W_OK) or not os.access(f, os.R_OK):
            if is_cli:
                pr.e(ansi.red + sys.argv[0] + ': permission is denied' + ansi.reset)
                pr.exit(1)
                return
            else:
                die_action()
                return
