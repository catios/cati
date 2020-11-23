#
# test_download_command.py
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

""" Test test_download_command """

import os
from TestCore import TestCore

class test_download_command(TestCore):
    """ Test test_download_command """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('download', ['gfdgghgf']), 1)

        self.assert_equals(self.run_command('repo', ['--scan', 'repository/test-repository']), 0)
        self.assert_equals(self.run_command('repo', ['--add', 'file://' + os.path.abspath('repository/test-repository') + ' name=main arch=all']), 0)

        self.assert_equals(self.run_command('update', []), 0)

        self.assert_equals(self.run_command('download', ['testpkgc']), 0)

        self.assert_true(os.path.isfile('testpkgc-2.0.cati'))
        os.remove('testpkgc-2.0.cati')

        self.assert_equals(self.run_command('download', ['testpkgc=2.0']), 0)

        self.assert_true(os.path.isfile('testpkgc-2.0.cati'))
        os.remove('testpkgc-2.0.cati')

        self.assert_equals(self.run_command('download', ['testpkgc=2.0', '--output=a.cati']), 0)

        self.assert_true(os.path.isfile('a.cati'))
        os.remove('a.cati')

        self.refresh_env()
