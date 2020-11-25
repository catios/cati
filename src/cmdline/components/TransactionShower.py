#
# TransactionShower.py
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

""" CLI transactions list shower """

from transaction.Calculator import Calculator
from cmdline import ansi, pr

def show(calc: Calculator):
    """
    shows transactions.

    gets a transaction.Calculator.Calculator object
    and shows list of calculated transactions
    (install/remove/upgrade/downgrade)
    """
    if calc.to_remove:
        pr.p('The following packages will be removed:')
        for pkg in calc.to_remove:
            pr.p('- ' + ansi.red + pkg.data['name'] + ansi.reset)
    # TODO : seprate upgrade and downgrade and install
    if calc.to_install:
        pr.p('The following packages will be installed:')
        for pkg in calc.to_install:
            pr.p('- ' + ansi.green + pkg.data['name'] + '(' + pkg.wanted_version + ')' + ansi.reset)
