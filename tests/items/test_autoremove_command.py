#
# test_autoremove_command.py
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

""" Test test_autoremove_command """

from TestCore import TestCore
from cati.package.Pkg import Pkg

class test_autoremove_command(TestCore):
    """ Test test_autoremove_command """
    def run(self):
        """ Run test """
        self.assert_equals(self.run_command('autoremove', []), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg11.cati',
            '--auto'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg10.cati',
        ]), 0)

        self.assert_true(Pkg.is_installed('testpkg11'))
        self.assert_true(Pkg.is_installed('testpkg10'))

        self.assert_equals(self.run_command('autoremove', ['-y']), 0)

        self.assert_true(Pkg.is_installed('testpkg11'))
        self.assert_true(Pkg.is_installed('testpkg10'))

        self.assert_equals(self.run_command('remove', [
            '-y',
            'testpkg10',
        ]), 0)

        self.assert_true(Pkg.is_installed('testpkg11'))
        self.assert_true(not Pkg.is_installed('testpkg10'))

        self.assert_equals(self.run_command('autoremove', ['-y']), 0)

        self.assert_true(not Pkg.is_installed('testpkg11'))
        self.assert_true(not Pkg.is_installed('testpkg10'))

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg11.cati',
            'repository/test-repository/testpkg10.cati',
            '--auto',
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg9.cati',
        ]), 0)

        self.assert_true(Pkg.is_installed('testpkg11'))
        self.assert_true(Pkg.is_installed('testpkg10'))
        self.assert_true(Pkg.is_installed('testpkg9'))

        self.assert_equals(self.run_command('remove', [
            '-y',
            'testpkg9',
        ]), 0)

        self.assert_true(Pkg.is_installed('testpkg11'))
        self.assert_true(Pkg.is_installed('testpkg10'))
        self.assert_true(not Pkg.is_installed('testpkg9'))

        self.assert_equals(self.run_command('autoremove', ['-y']), 0)

        self.assert_true(not Pkg.is_installed('testpkg11'))
        self.assert_true(not Pkg.is_installed('testpkg10'))
        self.assert_true(not Pkg.is_installed('testpkg9'))
