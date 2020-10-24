#
# PackageShower.py
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

from cmdline import ansi, pr

def show(data: dict):
    ''' Show transactions from calc '''
    output = ''
    output += 'Name: ' + ansi.green + data['name'] + ansi.reset + '\n'
    output += 'Version: ' + ansi.blue + data['version'] + ansi.reset + '\n'
    output += 'Arch: ' + ansi.yellow + data['arch'] + ansi.reset + '\n'
    try:
    	depends = data['depends']
    except:
    	depends = []
    if depends:
        output += 'Depends: '
        for dep in depends:
            output += dep + ', '
        output = output[:len(output)-2]
        output += '\n'
    try:
    	conflicts = data['conflicts']
    except:
    	conflicts = []
    if conflicts:
        output += 'Conflicts: '
        for conflict in conflicts:
            output += conflict + ', '
        output = output[:len(output)-2]
    pr.p(output)
