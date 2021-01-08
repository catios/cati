#
# StateContentShower.py
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

""" Shows and renders list of undoned transactions in state """

import sys
from cati.cmdline import pr, ansi
from cati.transaction.BaseTransaction import BaseTransaction

def show(state_list: list):
    """
    Shows and renders list of undoned transactions in state

    Args:
        state_list: loaded state from `transaction.BaseTransaction.state_list()` as (list)
    """
    pr.e(ansi.yellow + 'Error: state is not done')
    pr.p('\tthere is some undoned transactions:')
    for item in state_list:
        pr.p('\t\t' + BaseTransaction.state_item_to_string(item))
    pr.p('to complete them, run `' + sys.argv[0]  + ' state --complete`')
    pr.p(ansi.reset, end='')
