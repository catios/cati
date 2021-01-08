#
# Builder.py
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

""" Cati package builder """

import os
import json
import tarfile
from .exceptions import InvalidPackageDirException
from .ArchiveModel import archive_factory
from .PackageJsonValidator import PackageJsonValidator
from cati.frontend import Temp

class Builder:
    """ Cati package builder """

    @staticmethod
    def json_fields_are_valid(data: dict) -> bool:
        """
        alias for PackageJsonValidator.validate (validates package json info)

        Args:
            data: package data.json as dict
        
        Returns:
            returns boolean. True means json data is valid and False means invalid
        """
        return PackageJsonValidator.validate(data)

    def build(self, dirpath: str, output=None):
        """
        This function gets a directory and builds a .cati package from that.
        
        Args:
            dirpath: (str) package directory
            output: (str or None) path of the package output

        Raises:
            FileNotFoundError: when the directory not exists
            dotcati.exceptions.InvalidPackageDirException: when there is an probelm in package directory (problem will put as exception message)
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
            os.mkdir(dirpath + '/files')

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

        Args:
            dirpath: (str) package directory path
            output: (str) that filepath you want to compress file in that

        Raises:
            InvalidPackageDirException: when the output path is invalid
        """
        try:
            pkg = archive_factory(output, "w:gz")
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
