#
# test_channel_system.py
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

""" Test test_channel_system """

import os
from TestCore import TestCore
from package.Pkg import Pkg

class test_channel_system(TestCore):
    """ Test test_channel_system """
    def run(self):
        """ Run test """
        repo_path = os.getcwd() + '/repository/test-channels'

        self.assert_equals(self.run_command('repo', ['--scan', repo_path]), 0)

        repo = 'file://' + os.getcwd() + '/repository/test-channels arch=all pkg=cati'
        self.assert_equals(self.run_command('repo', ['--add', repo]), 0)
        self.assert_equals(self.run_command('update'), 0)
        pkg = Pkg.load_last('channelpkg')
        versions = pkg.get_versions_list()
        self.assert_equals(len(versions), 10)

        self.refresh_env()

        repo = 'file://' + os.getcwd() + '/repository/test-channels arch=all pkg=cati channel=dev'
        self.assert_equals(self.run_command('repo', ['--add', repo]), 0)
        self.assert_equals(self.run_command('update'), 0)
        pkg = Pkg.load_last('channelpkg')
        versions = pkg.get_versions_list()
        self.assert_equals(len(versions), 2)

        self.refresh_env()
        
        repo = 'file://' + os.getcwd() + '/repository/test-channels arch=all pkg=cati channel=dev,alpha'
        self.assert_equals(self.run_command('repo', ['--add', repo]), 0)
        self.assert_equals(self.run_command('update'), 0)
        pkg = Pkg.load_last('channelpkg')
        versions = pkg.get_versions_list()
        self.assert_equals(len(versions), 5)

        # test upgrade

        self.assert_equals(self.run_command('install', ['-y', 'channelpkg']), 0)
        pkg = Pkg.load_last('channelpkg')
        self.assert_equals(pkg.installed(), '1.0-alpha2')

        repo = 'file://' + os.getcwd() + '/repository/test-channels arch=all pkg=cati channel=release'
        self.assert_equals(self.run_command('repo', ['--add', repo]), 0)
        self.assert_equals(self.run_command('update'), 0)

        self.assert_equals(self.run_command('upgrade', ['-y']), 0)
        pkg = Pkg.load_last('channelpkg')
        self.assert_equals(pkg.installed(), '1.0')
