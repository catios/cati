#
# test_staticfile_system.py
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

""" Test test_staticfile_system """

from TestCore import TestCore

class test_staticfile_system(TestCore):
    """ Test test_staticfile_system """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/staticfile-pkg.cati',
        ]), 0)

        # check static file list content
        f = open(self.env() + '/var/lib/cati/installed/staticfile-pkg/staticfiles', 'r')
        content = f.read()
        f.close()
        self.assert_equals(
            content,
            'd0083d8df0fbb4a4bf8ba6c85a8155abd392314fe99b2b61cefe476a46a9af32@/usr/bin/test-cati-file'
        )

        self.refresh_env()
