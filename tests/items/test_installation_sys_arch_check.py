#
# test_installation_sys_arch_check.py
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

""" Test test_installation_sys_arch_check """

from TestCore import TestCore

class test_installation_sys_arch_check(TestCore):
    """ Test test_installation_sys_arch_check """
    def run(self):
        """ Run test """
        self.refresh_env()
        
        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/invalid-arch.cati'
        ]), 1)

        f = open(self.env() + '/etc/cati/allowed-architectures.list', 'w')
        f.write('aaa')
        f.close()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/invalid-arch.cati'
        ]), 0)

        self.refresh_env()
