#
# ArgParser.py
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

""" Cli argument parser """

from cati.cmdline import ansi

def parse(args: list) -> dict:
    """
    Gets a list from program arguments and returns parsed args

    Args:
        args: (list) command line arguments to parse that

    Returns:
        (dict) parsed arguments output structure:
        {
            ## all of arguments where starts with `-` (dict)
            "options": {
                "--option1": "value",
                "--option2": None, ## value will be None when option has not value
                ## ...
            },

            ## all of non-option arguemnt (list)
            "arguments": [
                "arg1",
                "arg2",
                ## ...
            ]
        }
    """

    # pop first argument (cati self exec)
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
        op_parts = option.split('=', 1)
        if len(op_parts) == 1:
            options[option] = None
        else:
            options[op_parts[0]] = op_parts[1]

    # check for --no-ansi
    i = 0
    for k in options:
        if k == '--no-ansi':
            del options[k]
            # disable ansi
            ansi.disable()
            break

    return {
        'options': options,
        'arguments': arguments
    }
