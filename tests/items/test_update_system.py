#
# test_update_system.py
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

""" Test test_update_system """

import os
from TestCore import TestCore
from package.Pkg import Pkg

class test_update_system(TestCore):
    """ Test test_update_system """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('update'), 0)

        self.assert_equals(self.run_command('repo', ['--scan', 'repository/test-repository']), 0)

        f = open(self.env() + '/etc/cati/repos.list', 'w')
        f.write('''
        file://''' + os.getcwd() + '''/repository/test-repository name=main arch=i386 pkg=cati
        ''')
        f.close()

        self.assert_equals(len(Pkg.all_list()['list']), 0)

        self.assert_equals(self.run_command('update'), 0)

        try:
            pkg_count = len(Pkg.all_list()['list'])
            self.assert_true(pkg_count == 9 or pkg_count == 10 or pkg_count == 8 or pkg_count == 7)
        except:
            print('Packages count:', pkg_count)
            raise

        f = open(self.env() + '/etc/cati/repos.list.d/repo-b', 'w')
        f.write('''
        file://''' + os.getcwd() + '''/repository/test-repository name=main-2 arch=all pkg=cati
        ''')
        f.close()

        try:
            pkg_count = len(Pkg.all_list()['list'])
            self.assert_true(pkg_count == 9 or pkg_count == 10 or pkg_count == 8 or pkg_count == 7)
        except:
            print('Packages count:', pkg_count)
            raise

        self.assert_equals(self.run_command('update'), 0)

        self.assert_equals(len(Pkg.all_list()['list']), 15)

        self.refresh_env()
