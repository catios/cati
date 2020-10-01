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

import tarfile, json

class ArchiveModel:
    ''' .cati package file model '''
    def __init__(self , file_path: str , type_str: str):
        self.tar = tarfile.open(file_path , type_str)
    
    def add(self , path , arcname=None):
        ''' Add a file to package archive '''
        return self.tar.add(path, arcname=arcname)

    def close(self):
        ''' Close package archive '''
        return self.tar.close()

    def members(self):
        files = []
        for member in self.tar.getmembers():
            if member.path != '':
                files.append(member.path)

        return files

    def read(self):
        self.data = self.info()

    def info(self):
        for member in self.tar.getmembers():
            if member.path == 'data.json':
                f = self.tar.extractfile(member)
                return json.loads(f.read())

