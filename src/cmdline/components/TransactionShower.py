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

    to_install = []
    to_upgrade = []
    to_downgrade = []
    to_reinstall = []
    for pkg in calc.to_install:
        if not pkg.installed():
            to_install.append(pkg)
        elif pkg.compare_version(pkg.wanted_version, pkg.installed()) == 1:
            to_upgrade.append(pkg)
        elif pkg.compare_version(pkg.wanted_version, pkg.installed()) == -1:
            to_downgrade.append(pkg)
        else:
            to_reinstall.append(pkg)
    if to_upgrade:
        pr.p('The following packages will be upgraded:')
        for pkg in to_upgrade:
            pr.p('- ' + ansi.yellow + pkg.data['name'] + '(' + pkg.installed() + ' -> ' + pkg.wanted_version + ')' + ansi.reset)

    if to_downgrade:
        pr.p('The following packages will be downgraded:')
        for pkg in to_downgrade:
            pr.p('- ' + ansi.yellow + pkg.data['name'] + '(' + pkg.installed() + ' >> ' + pkg.wanted_version + ')' + ansi.reset)

    if to_reinstall:
        pr.p('The following packages will be re-installed:')
        for pkg in to_reinstall:
            pr.p('- ' + ansi.yellow + pkg.data['name'] + '(' + pkg.wanted_version + ')' + ansi.reset)

    if to_install:
        pr.p('The following packages will be installed:')
        for pkg in to_install:
            pr.p('- ' + ansi.green + pkg.data['name'] + '(' + pkg.wanted_version + ')' + ansi.reset)
