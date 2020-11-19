#
# test_repo_command.py
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

""" Test test_repo_command """

from TestCore import TestCore
from repo.Repo import Repo

class test_repo_command(TestCore):
    """ Test test_repo_command """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('repo'), 0)

        f = open(self.env() + '/etc/cati/repos.list', 'w')
        f.write('''
        # The comment

        https://cati.example.com/packages name=main-repo pkg=cati arch=amd64 priority=10 # another comment

        https://cati.example2.com/packages name=test-repo pkg=deb arch=i386
        https://cati.example2.com/packages2 name=test-repo2 pkg=deb arch=all priority=2 # all
        ''')
        f.close()

        self.assert_equals(self.run_command('repo'), 0)

        repos = Repo.get_list()

        self.assert_equals(len(repos), 3)

        self.assert_equals(repos[0].name, 'test-repo')
        self.assert_equals(repos[0].pkg, 'deb')
        self.assert_equals(repos[0].arch, 'i386')
        self.assert_equals(int(repos[0].priority), 1)

        self.assert_equals(repos[1].name, 'test-repo2')
        self.assert_equals(repos[1].pkg, 'deb')
        self.assert_equals(repos[1].arch, 'all')
        self.assert_equals(int(repos[1].priority), 2)

        self.assert_equals(repos[2].name, 'main-repo')
        self.assert_equals(repos[2].pkg, 'cati')
        self.assert_equals(repos[2].arch, 'amd64')
        self.assert_equals(int(repos[2].priority), 10)

        f = open(self.env() + '/etc/cati/repos.list.d/test', 'w')
        f.write('''
        file:///test name=test pkg=cati arch=amd64 priority=11 # another comment
        ''')
        f.close()

        self.assert_equals(len(Repo.get_list()), 4)

        f = open(self.env() + '/etc/cati/repos.list.d/test', 'w')
        f.write('''
        file:///test phgfhgf name=test pkg=cati arch priority=100
        ''')
        f.close()

        self.assert_equals(len(Repo.get_list()[-1].syntax_errors), 2)

        self.refresh_env()

        f = open(self.env() + '/etc/cati/repos.list', 'w')
        f.write('''
        file/test phgfhgf namgdfhhe=test pk pritgh
        ''')
        f.close()

        self.assert_equals(Repo.get_list()[-1].successful_loaded, False)

        self.refresh_env()
