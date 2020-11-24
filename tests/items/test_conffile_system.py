#
# test_conffile_system.py
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

""" Test test_conffile_system """

import os
from TestCore import TestCore

class test_conffile_system(TestCore):
    """ Test test_conffile_system """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg.cati'
        ]), 0)

        self.assert_true(
            os.path.isfile(self.env() + '/etc/cati-test-pkg/a.conf') and\
            os.path.isfile(self.env() + '/etc/cati-test-pkg/test.txt') and\
            os.path.isfile(self.env() + '/etc/cati-test-pkg/dir/hello.list')
        )

        self.assert_equals(self.run_command('remove', [
            'conffile-pkg',
            '-y',
        ]), 0)

        self.assert_true(os.path.isfile(self.env() + '/etc/cati-test-pkg/a.conf'))
        self.assert_true(os.path.isfile(self.env() + '/etc/cati-test-pkg/dir/hello.list'))
        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/test.txt'))

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg.cati'
        ]), 0)

        self.assert_true(
            os.path.isfile(self.env() + '/etc/cati-test-pkg/a.conf') and\
            os.path.isfile(self.env() + '/etc/cati-test-pkg/test.txt') and\
            os.path.isfile(self.env() + '/etc/cati-test-pkg/dir/hello.list')
        )

        self.assert_equals(self.run_command('remove', [
            'conffile-pkg',
            '-y',
            '--conffiles',
        ]), 0)

        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/a.conf'))
        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/dir/hello.list'))
        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/test.txt'))

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg.cati'
        ]), 0)

        self.assert_true(
            os.path.isfile(self.env() + '/etc/cati-test-pkg/a.conf') and\
            os.path.isfile(self.env() + '/etc/cati-test-pkg/test.txt') and\
            os.path.isfile(self.env() + '/etc/cati-test-pkg/dir/hello.list')
        )

        self.assert_equals(self.run_command('remove', [
            'conffile-pkg',
            '-y',
        ]), 0)

        self.assert_true(os.path.isfile(self.env() + '/etc/cati-test-pkg/a.conf'))
        self.assert_true(os.path.isfile(self.env() + '/etc/cati-test-pkg/dir/hello.list'))
        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/test.txt'))

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg.cati'
        ]), 0)

        self.assert_equals(self.run_command('remove', [
            'conffile-pkg',
            '-y',
            '--conffiles',
        ]), 0)

        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/a.conf'))
        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/dir/hello.list'))
        self.assert_true(not os.path.isfile(self.env() + '/etc/cati-test-pkg/test.txt'))

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg.cati'
        ]), 0)

        f = open(self.env() + '/var/lib/cati/installed/conffile-pkg/conffiles', 'r')
        content = f.read()
        f.close()

        try:
            self.disable_raising()
            self.assert_equals(content.strip(), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855@/etc/cati-test-pkg/dir/hello.list\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855@/etc/cati-test-pkg/a.conf')
        except:
            self.enable_raising()
            self.assert_equals(content.strip(), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855@/etc/cati-test-pkg/a.conf\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855@/etc/cati-test-pkg/dir/hello.list')
        self.enable_raising()

        f = open(self.env() + '/etc/cati-test-pkg/dir/hello.list', 'w')
        f.write('hello')
        f.close()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg.cati'
        ]), 0)

        f = open(self.env() + '/etc/cati-test-pkg/dir/hello.list', 'r')
        content = f.read().strip()
        f.close()
        self.assert_equals(content, 'hello')

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg-1.1.cati'
        ]), 0)

        f = open(self.env() + '/etc/cati-test-pkg/dir/hello.list', 'r')
        content = f.read().strip()
        f.close()
        self.assert_equals(content, 'new content')

        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/conffile-pkg.cati'
        ]), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            '--keep-conffiles',
            'tests/test-packages/packages/conffile-pkg-1.1.cati'
        ]), 0)

        f = open(self.env() + '/etc/cati-test-pkg/dir/hello.list', 'r')
        content = f.read().strip()
        f.close()
        self.assert_equals(content, '')

        self.refresh_env()
