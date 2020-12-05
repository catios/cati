#
# test_rdepends_command.py
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

""" Test test_rdepends_command """

from TestCore import TestCore

class test_rdepends_command(TestCore):
    """ Test test_rdepends_command """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('rdepends', [
            'fgghfghfghf',
        ]), 1)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg11.cati',
            'tests/test-packages/packages/testpkg10.cati',
        ]), 0)

        self.assert_equals(self.run_command('rdepends', [
            'testpkg11',
        ]), 0)

        self.assert_equals(self.run_command('rdepends', [
            'testpkg11', 'hgfhgjgh'
        ]), 0)

        self.assert_equals(self.run_command('rdepends', [
            'testpkg11', 'testpkg10'
        ]), 0)

        self.assert_equals(self.run_command('rdepends', [
            'testpkg11', 'testpkg10', '-q'
        ]), 0)

        self.assert_equals(self.run_command('rdepends', [
            'testpkg11', 'testpkg10', '--quiet'
        ]), 0)

        self.refresh_env()
