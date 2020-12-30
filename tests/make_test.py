#!/usr/bin/env python3
#
# make_test.py
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

""" Test maker """

import sys
import os

test_template = '''""" Test <testname> """

from TestCore import TestCore

class <testname>(TestCore):
    """ Test <testname> """
    def run(self):
        """ Run test """
        self.assert_true(True)
'''

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Please enter name of test as argument')
        sys.exit(1)
    
    # create test
    f = open('tests/items/' + sys.argv[1] + '.py', 'w')
    f.write(test_template.replace('<testname>', sys.argv[1]))
    f.close()

    print('Test was created successfuly')
