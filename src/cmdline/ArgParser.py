#
# ArgParser.py
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

''' Cli argument parser '''

def parse(args: list) -> dict:
    ''' Gets a list from program arguments and returns parsed args '''

    args.pop(0)

    tmp_options = []
    arguments = []

    # split options & arguments
    for arg in args:
        if arg[0] == '-':
            tmp_options.append(arg)
        else:
            arguments.append(arg)

    options = {}
    for option in tmp_options:
        op_parts = option.split('=' , 1)
        if len(op_parts) == 1:
            options[option] = None
        else:
            options[op_parts[0]] = op_parts[1]

    return {
        'options': options,
        'arguments': arguments
    }
