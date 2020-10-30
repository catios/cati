#
# PackageJsonValidator.py
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

""" Package information json validator """

class PackageJsonValidator:
    """ Package information json validator """
    @staticmethod
    def validate(data: dict) -> bool:
        """
        This function gets a json object and checks that fields and value of them where
        are required for a valid package data.json and says this data
        is valid or not
        """

        try:
            # TODO : check more fields
            assert type(data['name']) == str
            assert type(data['version']) == str
            assert type(data['arch']) == str

            try:
                tmp = data['depends']
                try:
                    assert type(data['depends']) == list
                except:
                    raise
            except:
                pass

            try:
                tmp = data['conflicts']
                try:
                    assert type(data['conflicts']) == list
                except:
                    raise
            except:
                pass

            try:
                tmp = data['description']
                try:
                    assert type(data['description']) == str
                except:
                    raise
            except:
                pass

            try:
                tmp = data['author']
                try:
                    assert type(data['author']) == str
                    assert not '|' in data['author']
                except:
                    raise
            except:
                pass

            try:
                tmp = data['maintainer']
                try:
                    assert type(data['maintainer']) == str
                    assert not '|' in data['maintainer']
                except:
                    raise
            except:
                pass

            try:
                tmp = data['homepage']
                try:
                    assert type(data['homepage']) == str
                except:
                    raise
            except:
                pass

            try:
                tmp = data['category']
                try:
                    assert type(data['category']) == list
                except:
                    raise
            except:
                pass

            try:
                tmp = data['channel']
                try:
                    assert type(data['channel']) == str
                except:
                    raise
            except:
                pass

            return True
        except:
            return False
