#!/usr/bin/env python3
#
# cati.py
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

""" Cati main cli entry point """

import sys
from cmdline import kernel, pr, ansi
from frontend import HealthChecker

# check cati installation health
def cati_installation_is_corrupt(filepath: str, filetype: str):
    """
    Will run when cati installation is corrupt
    shows error to user
    """
    pr.e(ansi.red + 'Cati installation is corrupt. to repair it, just run cati with root access' + ansi.reset)
    pr.exit(1)

HealthChecker.check({
    'failed_to_repair': cati_installation_is_corrupt,
})

# handle cli
kernel.handle(sys.argv[:])
