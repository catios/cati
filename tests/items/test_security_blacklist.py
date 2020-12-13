#
# test_security_blacklist.py
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

""" Test test_security_blacklist """

from TestCore import TestCore

class test_security_blacklist(TestCore):
    """ Test test_security_blacklist """
    def run(self):
        """ Run test """
        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/some-malware.cati'
        ]), 0)

        f = open(self.env() + '/var/lib/cati/security-blacklist/1.json', 'w')
        f.write('''[
            {
                "title": "test-malware",
                "description": "description of some-malware",
                "md5": "d5a86c337ec5d02062a93aee89f6a291",
                "sha256": "9997a794d859c60993b0c3a860cbd17451f24a16da8aa094bccfe9a0fcc9d86f",
                "sha512": "4db5647668b0fd8f6dedca518133eb1dacaaf6e2c9fbb17032215831de970a117d7be252d153d4d755edf73c05f9af618de862bc54ca4d1e8893b0afc652af29"
            }
        ]''')
        f.close()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/some-malware.cati'
        ]), 1)

        self.assert_equals(self.run_command('pkg', [
            'install',
            '--force',
            'repository/test-repository/some-malware.cati'
        ]), 0)
