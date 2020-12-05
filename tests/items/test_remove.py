#
# test_remove.py
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

""" Test test_remove """

from TestCore import TestCore
from package.Pkg import Pkg

class test_remove(TestCore):
    """ Test test_remove """
    def run(self):
        """ Run test """

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg10.cati'
        ]), 1)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg11.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg10.cati'
        ]), 0)

        self.assert_true(Pkg.is_installed('testpkg10'))
        self.assert_true(Pkg.is_installed('testpkg11'))

        self.assert_equals(self.run_command('remove', [
            'testpkg10',
            '-y'
        ]), 0)

        self.assert_true(not Pkg.is_installed('testpkg10'))
        self.assert_true(Pkg.is_installed('testpkg11'))

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg10.cati'
        ]), 0)

        self.assert_true(Pkg.is_installed('testpkg10'))
        self.assert_true(Pkg.is_installed('testpkg11'))

        self.assert_equals(self.run_command('remove', [
            'testpkg11',
            '-y'
        ]), 0)

        self.assert_true(not Pkg.is_installed('testpkg10'))
        self.assert_true(not Pkg.is_installed('testpkg11'))

        self.refresh_env()
        
        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/essential-package.cati'
        ]), 0)

        self.assert_true(Pkg.is_installed('essential-package'))

        self.assert_equals(self.run_command('remove', [
            'essential-package',
            '-y'
        ]), 1)

        self.assert_true(Pkg.is_installed('essential-package'))

        self.assert_equals(self.run_command('remove', [
            'essential-package',
            '-y',
            '--force'
        ]), 0)

        self.assert_true(not Pkg.is_installed('essential-package'))

        self.refresh_env()
