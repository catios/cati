#
# PackageJsonValidator.py
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

""" Package information json validator """

class PackageJsonValidator:
    """ Package information json validator """
    @staticmethod
    def validate(data: dict) -> bool:
        """
        This function gets a json object and checks that fields and value of them where
        are required for a valid package data.json and says this data
        is valid or not

        Args:
            data: package data.json as dictonary

        Returns:
            boolean. True means data is valid and False means data is invalid
        """

        try:
            assert type(data['name']) == str
            assert type(data['version']) == str
            assert type(data['arch']) == str

            try:
                tmp = data['depends']
                try:
                    assert type(data['depends']) == list
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['conflicts']
                try:
                    assert type(data['conflicts']) == list
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['suggests']
                try:
                    assert type(data['suggests']) == list
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['conffiles']
                try:
                    assert type(data['conffiles']) == list
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['staticfiles']
                try:
                    assert type(data['staticfiles']) == list
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['description']
                try:
                    assert type(data['description']) == str
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['author']
                try:
                    assert type(data['author']) == str
                    assert not '|' in data['author']
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['maintainer']
                try:
                    assert type(data['maintainer']) == str
                    assert not '|' in data['maintainer']
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['homepage']
                try:
                    assert type(data['homepage']) == str
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['category']
                try:
                    assert type(data['category']) == list
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['channel']
                try:
                    assert type(data['channel']) == str
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['uploaders']
                try:
                    assert type(data['uploaders']) == list
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['changed-by']
                try:
                    assert type(data['changed-by']) == str
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['changes']
                try:
                    assert type(data['changes']) == str
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                tmp = data['date']
                try:
                    assert type(data['date']) == str
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                urgency = data['urgency']
                try:
                    assert type(data['urgency']) == str
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                installed_size = data['installed-size']
                try:
                    assert type(data['installed-size']) == int
                except:
                    raise
            except KeyError as ex:
                pass

            try:
                essential = data['essential']
                try:
                    assert type(data['essential']) == bool
                except:
                    raise
            except KeyError as ex:
                pass

            return True
        except:
            return False
