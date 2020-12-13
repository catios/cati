#
# test_list_command.py
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

""" Test test_list_command """

from TestCore import TestCore

class test_list_command(TestCore):
    """ Test test_list_command """
    def run(self):
        """ Run test """
        self.assert_equals(self.run_command('list'), 0)
        self.assert_equals(self.run_command('list', ['--installed']), 0)
        self.assert_equals(self.run_command('list', ['--installed-manual']), 0)
        self.assert_equals(self.run_command('list', ['-q']), 0)
        self.assert_equals(self.run_command('list', ['--quiet']), 0)
        self.assert_equals(self.run_command('list', ['-v']), 0)
        self.assert_equals(self.run_command('list', ['--verbose']), 0)
        self.assert_equals(self.run_command('list', ['--author="author1"']), 0)
        self.assert_equals(self.run_command('list', ['--author="author1|author2"']), 0)
        self.assert_equals(self.run_command('list', ['--maintainer="maintainer1"']), 0)
        self.assert_equals(self.run_command('list', ['--maintainer="maintainer1|maintainer2"']), 0)
        self.assert_equals(self.run_command('list', ['--category="category1"']), 0)
        self.assert_equals(self.run_command('list', ['--category="category1|category2"']), 0)
        self.assert_equals(self.run_command('list', ['--search="theword"']), 0)
        self.assert_equals(self.run_command('list', ['--search="the test word"']), 0)
