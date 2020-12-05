#
# test_package_any_script.py
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

""" Test test_package_any_script """

import os
from TestCore import TestCore

class test_package_any_script(TestCore):
    """ Test test_package_any_script """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg-with-any-script.cati'
        ]), 0)

        self.assert_true(os.path.isfile(self.env() + '/var/lib/cati/any-scripts/testpkg-with-any-script'))

        self.assert_equals(self.run_command('remove', [
            'testpkg-with-any-script',
            '-y'
        ]), 0)

        self.assert_true(not os.path.isfile(self.env() + '/var/lib/cati/any-scripts/testpkg-with-any-script'))

        os.remove('temp')

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg-with-any-script.cati'
        ]), 0)

        self.assert_true(os.path.isfile('temp'))
        os.remove('temp')

        self.assert_equals(self.run_command('remove', [
            'testpkg-with-any-script',
            '-y'
        ]), 0)
        self.assert_true(not os.path.isfile('temp'))

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg-with-any-script.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkgc-2.0.cati'
        ]), 0)

        os.remove('temp')

        self.assert_equals(self.run_command('remove', [
            'testpkgc',
            '-y'
        ]), 0)

        self.assert_true(os.path.isfile('temp'))
        os.remove('temp')

        self.refresh_env()
