#
# test_depends_and_conflicts.py
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

""" Test test_depends_and_conflicts """

import os
from TestCore import TestCore

class test_depends_and_conflicts(TestCore):
    """ Test test_depends_and_conflicts """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgb-1.0.cati'
        ]), 1)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgb-1.1.cati'
        ]), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgb-1.2.cati'
        ]), 0)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgc-1.0.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgb-1.3.cati'
        ]), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgc-2.0.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgb-1.3.cati'
        ]), 0)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgb-1.2.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgc-2.0.cati'
        ]), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-depend.cati'
        ]), 1)

        f = open(self.env() + '/etc/testfile', 'w')
        f.write('')
        f.close()
        f = open(self.env() + '/etc/anotherfile', 'w')
        f.write('hello\n')
        f.close()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-depend.cati'
        ]), 0)

        self.refresh_env()

        f = open(self.env() + '/etc/testfile', 'w')
        f.write('')
        f.close()
        f = open(self.env() + '/etc/anotherfile', 'w')
        f.write('hello\n')
        f.close()
        f = open(self.env() + '/etc/filea', 'w')
        f.write('')
        f.close()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg-with-file-depend.cati'
        ]), 1)

        self.refresh_env()
