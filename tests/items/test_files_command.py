#
# test_files_command.py
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

""" Test test_files_command """

from TestCore import TestCore

class test_files_command(TestCore):
    """ Test test_files_command """
    def run(self):
        """ Run test """
        self.assert_equals(self.run_command('files', ['gfdgfhghgfh']), 1)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgc-2.0.cati'
        ]), 0)

        self.assert_equals(self.run_command('files', ['testpkgc']), 0)
        self.assert_equals(self.run_command('files', ['testpkgc', 'gfgfhfg']), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg11.cati'
        ]), 0)

        self.assert_equals(self.run_command('files', ['testpkg11']), 0)
        self.assert_equals(self.run_command('files', ['testpkgc', 'testpkg11']), 0)
        self.assert_equals(self.run_command('files', ['testpkgc', 'fgfhghfhhgj', 'testpkg11']), 0)

        self.assert_equals(self.run_command('files', ['testpkgc=2.0']), 0)
        self.assert_equals(self.run_command('files', ['testpkgc=1.0']), 1)

        self.assert_equals(self.run_command('files', ['testpkgc', 'testpkg11', '-q']), 0)
        self.assert_equals(self.run_command('files', ['testpkgc', 'testpkg11', '--quiet']), 0)

        self.assert_equals(self.run_command('files', ['--installed']), 0)
        self.assert_equals(self.run_command('files', ['--installed', '-q']), 0)
        self.assert_equals(self.run_command('files', ['--installed', '--quiet']), 0)
