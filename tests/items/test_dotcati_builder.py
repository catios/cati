#
# test_dotcati_builder.py
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

""" Test test_dotcati_builder """

from TestCore import TestCore

import os
from dotcati.ArchiveModel import ArchiveModel

class test_dotcati_builder(TestCore):
    """ Test test_dotcati_builder """
    def run(self):
        """ Run test """

        self.assert_equals(self.run_command(
        	'pkg',
        	[
        		'build',
        		'repository/test-packages/build/notfound',
        		'--output=repository/test-packages/output/testpkga-1.0.cati'
        	]
        ), 1)

        self.assert_equals(self.run_command(
            'pkg',
            [
                'build',
                'repository/test-packages/build/testpkga/1.0',
                '--output=repository/test-packages/output/notfound/test'
            ]
        ), 1)

        self.assert_equals(self.run_command(
        	'pkg',
        	[
        		'build',
        		'repository/test-packages/build/testpkga/1.0',
        		'--output=repository/test-packages/output/testpkga-1.0.cati'
        	]
        ), 0)

        self.assert_true(
        	os.path.isfile('repository/test-packages/output/testpkga-1.0.cati')
        )

        try:
            pkg = ArchiveModel('repository/test-packages/output/testpkga-1.0.cati', 'r')
            pkg.read()
            self.assert_equals(pkg.data['name'], 'testpkga')
            self.assert_equals(pkg.data['version'], '1.0')
            self.assert_equals(pkg.data['arch'], 'i386')
            tmp = pkg.members()
            tmp.sort()
            self.assert_equals(tmp, [
                'data.json',
                'files',
                'files/usr',
                'files/usr/bin',
                'files/usr/bin/cati-testpkga',
            ])
        except:
            # created file is corrupt
            self.assert_true(False)

        self.assert_equals(self.run_command(
            'pkg',
            [
                'build',
                'repository/test-packages/build/testpkga/1.1-corrupt',
                '--output=repository/test-packages/output/testpkga-1.0.cati'
            ]
        ), 1)
