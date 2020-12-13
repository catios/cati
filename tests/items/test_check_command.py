#
# test_check_command.py
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

""" Test test_check_command """

import os
from TestCore import TestCore

class test_check_command(TestCore):
    """ Test test_check_command """
    def run(self):
        """ Run test """
        self.assert_equals(self.run_command('check', []), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgc-2.0.cati'
        ]), 0)

        self.assert_equals(self.run_command('check', []), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/staticfile-pkg.cati'
        ]), 0)

        self.assert_equals(self.run_command('check', []), 0)

        f = open(self.env() + '/usr/bin/test-cati-file', 'w')
        f.write('aaa')
        f.close()

        self.assert_equals(self.run_command('check', []), 1)

        f = open(self.env() + '/usr/bin/test-cati-file', 'w')
        f.write('hello world.\n')
        f.close()

        self.assert_equals(self.run_command('check', []), 0)

        os.remove(self.env() + '/usr/bin/test-cati-file')

        self.assert_equals(self.run_command('check', []), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/staticfile-pkg.cati'
        ]), 0)

        self.assert_equals(self.run_command('check', []), 0)

        os.remove(self.env() + '/var/lib/cati/installed/staticfile-pkg/ver')

        self.assert_equals(self.run_command('check', []), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('check', []), 0)

        os.mkdir(self.env() + '/var/lib/cati/security-blacklist/thedir')

        self.assert_equals(self.run_command('check', []), 1)

        self.refresh_env()

        self.assert_equals(self.run_command('check', []), 0)

        f = open(self.env() + '/var/lib/cati/security-blacklist/a.json', 'w')
        f.write('badjson')
        f.close()

        self.assert_equals(self.run_command('check', []), 1)

        f = open(self.env() + '/var/lib/cati/security-blacklist/a.json', 'w')
        f.write('[]')
        f.close()

        self.assert_equals(self.run_command('check', []), 0)
