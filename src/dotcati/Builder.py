#
# Builder.py
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

""" Cati package builder """

import os
import json
import tarfile
from dotcati.exceptions import InvalidPackageDirException
from dotcati.ArchiveModel import ArchiveModel
from dotcati.PackageJsonValidator import PackageJsonValidator
from frontend import Temp

class Builder:
    """ Cati package builder """

    @staticmethod
    def json_fields_are_valid(data: dict):
        """ alias for PackageJsonValidator.validate (validates package json info) """
        return PackageJsonValidator.validate(data)

    def build(self, dirpath: str, output=None):
        """
        This function gets a directory and builds a .cati package from that
        the output is optional parameter. this argument can be used
        to set package output file.

        will raise InvalidPackageDirException when there is an probelm in package directory (problem will put as exception message)
        """

        if not os.path.isdir(dirpath):
            raise FileNotFoundError

        if not os.path.isfile(dirpath + '/data.json'):
            raise InvalidPackageDirException('file data.json not found')

        # validate data.json content
        try:
            data_json_content = open(dirpath + '/data.json', 'r').read()
        except:
            raise InvalidPackageDirException('cannot read data.json')

        try:
            data_json = json.loads(data_json_content)
        except:
            raise InvalidPackageDirException('invalid json syntax in data.json')

        if not self.json_fields_are_valid(data_json):
            raise InvalidPackageDirException('one or more fields in data.json is invalid')

        if not os.path.isdir(dirpath + '/files'):
            raise InvalidPackageDirException('directory files not found')

        # compress and build package
        if output == None:
            # set default output file
            output = ''
            if dirpath[-1] == '/':
                output = dirpath[:-1]
            else:
                output = dirpath

            output += '.cati'

        self.compress(dirpath, output)

        return output

    def compress(self, dirpath: str, output: str):
        """
        This function compresses content of target directory and build package
        in output file
        """
        try:
            pkg = ArchiveModel(output, "w:gz")
        except:
            raise InvalidPackageDirException('file "' + output + '" for output of package not found')

        pkg.add(dirpath, arcname='/')
        # add `cati-version` file
        cati_version_tmp_f = Temp.make_file()
        tmp_f = open(cati_version_tmp_f, 'w')
        tmp_f.write('1.0')
        tmp_f.close()
        pkg.add(cati_version_tmp_f, arcname='/')
        pkg.close()
