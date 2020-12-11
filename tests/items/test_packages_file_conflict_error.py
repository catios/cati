#
# test_packages_file_conflict_error.py
#
# the cati project
# Copyright 2020 parsa shahmaleki <parsampsh@gmail.com>
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

""" Test test_packages_file_conflict_error """

from TestCore import TestCore

class test_packages_file_conflict_error(TestCore):
    """ Test test_packages_file_conflict_error """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-conflict-a.cati'
        ]), 0)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-conflict-b.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-conflict-a.cati'
        ]), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-conflict-a.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-conflict-b.cati'
        ]), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-conflict-a.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-conflict-b-replaces.cati'
        ]), 0)

        self.refresh_env()
