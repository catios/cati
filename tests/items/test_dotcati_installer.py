#
# test_dotcati_installer.py
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

""" Test test_dotcati_installer """

from TestCore import TestCore
import os
import json
from package.Pkg import Pkg
from frontend import Env

class test_dotcati_installer(TestCore):
    """ Test test_dotcati_installer """
    def run(self):
        """ Run test """
        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/simple-test-package.cati'
        ]), 0)

        self.assert_true(os.path.isfile(self.env('/usr/bin/cati-testpkga')))

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/simple-test-package.cati'
        ]), 0)

        self.assert_true(os.path.isfile(self.env('/usr/bin/cati-testpkga')))

        pkg = Pkg.load_from_index(json.loads(open(Env.packages_lists('/testpkga/index'), 'r').read()), 'testpkga')
        self.assert_equals(pkg.installed(), '1.0')

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg-with-file-conflict-a.cati',
        ]), 0)

        self.assert_true(os.path.isfile(self.env() + '/etc/testpkg-with-file-conflict/test.txt'))

        self.refresh_env()

        os.mkdir(self.env() + '/app')

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkg-with-file-conflict-a.cati',
            '--target=/app'
        ]), 0)

        self.assert_true(not os.path.isfile(self.env() + '/etc/testpkg-with-file-conflict/test.txt'))
        self.assert_true(os.path.isfile(self.env() + '/app/etc/testpkg-with-file-conflict/test.txt'))

        self.refresh_env()
