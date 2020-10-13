#
# pr.py
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

''' Print handling in cli '''

import sys

def p(value, end='\n'):
    ''' Print on stdout '''
    return print(value, end=end, flush=True)

def e(value, end='\n'):
    ''' Print on stderr '''
    return print(value, end=end, flush=True, file=sys.stderr)

def exit(code=0):
    ''' Exits program with exit code '''
    sys.exit(code)
