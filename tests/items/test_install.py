#
# test_install.py
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

""" Test test_install """

import os
from TestCore import TestCore
from package.Pkg import Pkg

class test_install(TestCore):
    """ Test test_install """
    def run(self):
        """ Run test """
        self.refresh_env()

        repo1 = "file://" + os.getcwd() + '/repository name=test arch=all pkg=cati'
        repo2 = "file://" + os.getcwd() + '/repository name=test arch=i386 pkg=cati'

        self.assert_equals(self.run_command('repo', ['--scan', os.getcwd() + '/repository']), 0)

        self.assert_equals(self.run_command('repo', ['--add', repo1]), 0)
        self.assert_equals(self.run_command('repo', ['--add', repo2]), 0)
        self.assert_equals(self.run_command('update'), 0)

        self.assert_equals(self.run_command('install', ['testpkg10', '-y']), 0)

        self.assert_true(Pkg.is_installed('testpkg10'))
        self.assert_true(Pkg.is_installed('testpkg11'))

        self.assert_equals(self.run_command('install', ['testpkgb', '-y']), 0)

        self.assert_true(Pkg.is_installed('testpkgb'))
        self.assert_true(Pkg.is_installed('testpkgc'))
        self.assert_true(not Pkg.is_installed_manual('testpkgc'))

        self.assert_equals(self.run_command('install', ['testpkgz', '-y']), 0)

        self.assert_true(not Pkg.is_installed('testpkgb'))
        self.assert_true(not Pkg.is_installed('testpkgc'))
        self.assert_true(Pkg.is_installed('testpkgz'))

        self.assert_equals(self.run_command('install', ['testpkgb', '-y']), 0)

        self.assert_true(Pkg.is_installed('testpkgb'))
        self.assert_true(Pkg.is_installed('testpkgc'))
        self.assert_true(not Pkg.is_installed('testpkgz'))

        self.assert_equals(self.run_command('remove', ['testpkgb', 'testpkgc', '-y']), 0)

        # test upgrade
        self.assert_equals(self.run_command('install', ['testpkgc=1.0', '-y']), 0)

        testpkgc = Pkg.load_last('testpkgc')
        self.assert_equals(testpkgc.installed(), '1.0')

        self.assert_equals(self.run_command('upgrade', ['-y']), 0)

        testpkgc = Pkg.load_last('testpkgc')
        self.assert_equals(testpkgc.installed(), '2.0')

        self.refresh_env()
