#
# ArchiveModel.py
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

''' .cati package file model '''

import tarfile
import json
from dotcati.PackageJsonValidator import PackageJsonValidator

class ArchiveModel:
    ''' .cati package file model '''
    def __init__(self, file_path: str, type_str: str):
        self.tar = tarfile.open(file_path, type_str)

    def add(self, path, arcname=None):
        ''' Add a file to package archive '''
        return self.tar.add(path, arcname=arcname)

    def close(self):
        ''' Close package archive '''
        return self.tar.close()

    def members(self):
        ''' Returns members of the archive '''
        files = []
        for member in self.tar.getmembers():
            if member.path != '':
                files.append(member.path)

        return files

    def read(self):
        ''' Load package information on object '''
        self.data = self.info()
        if not PackageJsonValidator.validate(self.data):
            raise

    def extractall(self, path):
        ''' Extract all of package files to `path` '''
        return self.tar.extractall(path)

    def info(self) -> dict:
        ''' Returns package data.json information '''
        for member in self.tar.getmembers():
            if member.path == 'data.json':
                f = self.tar.extractfile(member)
                return json.loads(f.read())

    def pkg_version(self) -> str:
        ''' Returns dotcati package strcuture version '''
        for member in self.tar.getmembers():
            if member.path == 'cati-version':
                # load dotcati package version
                f = self.tar.extractfile(member)
                return f.read().strip()

        # default version
        return '1.0'
