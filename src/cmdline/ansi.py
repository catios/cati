#
# ansi.py
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

""" ANSI terminal colors """

header = '\033[95m'
"""
header
"""

blue = '\033[94m'
"""
blue
"""

green = '\033[92m'
"""
green
"""

yellow = '\033[93m'
"""
yellow
"""

red = '\033[91m'
"""
red
"""

reset = '\033[0m'
"""
reset
"""

bold = '\033[1m'
"""
bold
"""

underline = '\033[4m'
"""
underline
"""

cyan = '\033[96m'
"""
cyan
"""

def disable():
    """
    disable ansi characters.
    assign null value to all of ansi chars to disable them
    """
    from cmdline import ansi
    ansi.header = ''
    ansi.blue = ''
    ansi.green = ''
    ansi.yellow = ''
    ansi.red = ''
    ansi.reset = ''
    ansi.bold = ''
    ansi.underline = ''
    ansi.cyan = ''
