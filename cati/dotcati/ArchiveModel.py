#
# ArchiveModel.py
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

""" .cati package archive handling """

import os
import mimetypes
import tarfile
import json
from .PackageJsonValidator import PackageJsonValidator
from .Pkg import Pkg
from . import PkgConvertor

class BaseArchive(Pkg):
    """ base archive for archive versions """
    def __init__(self, file_path: str, type_str: str):
        self.tar = tarfile.open(file_path, type_str)

    def add(self, path: str, arcname=None):
        """
        Add a file to package archive (in `w` mode)

        Args:
            path: that file you want to add
            arcname: the arcname
        """
        return self.tar.add(path, arcname=arcname)

    def close(self):
        """ Close package archive """
        return self.tar.close()

    def extractall(self, path: str):
        """ Extract all of package files to `path` arg """
        return self.tar.extractall(path)

    def pkg_version(self) -> str:
        """
        Returns dotcati package strcuture version

        Returns:
            '1.0' str
        """
        for member in self.tar.getmembers():
            if member.path == 'cati-version':
                # load dotcati package version
                f = self.tar.extractfile(member)
                return f.read().strip()
        # default version
        return '1.0'

    def members(self) -> list:
        """
        Returns members of the archive as paths string

        Returns:
            list[str] list of path strings
        """
        files = []
        for member in self.tar.getmembers():
            if member.path != '':
                files.append(member.path)
        return files

    def read(self):
        """
        Load package information on object.
        
        This method has not arg or output, just loads some information of package to this object.

        Raises:
            Exception: will raise normal Exception when package json data is invalid
                       (validated by dotcati.PackageJsonValidator.validate())
        """
        self.data = self.info()
        if not PackageJsonValidator.validate(self.data):
            raise
        # try to compare version for version validation
        Pkg.compare_version(self.data['version'], '0.0.0')
        self.data['version'] = self.data['version'].strip()

    def info(self) -> (dict, None):
        """ Returns package data.json information """
        for member in self.tar.getmembers():
            if member.path == 'data.json':
                f = self.tar.extractfile(member)
                return json.loads(f.read())
        return None

def archive_factory(file_path: str, type_str: str) -> BaseArchive:
    """
    Archive model factory. Loads a package archive from file

    the strcuture of packages, maybe change in new version of cati.
    so, cati should be compatible with old packages where
    created with old version of cati. this class
    is a factory to check package version and
    return archive model object by that
    version.

    Args:
        file_path: (str) archive filepath
        type_str: (str) open type of archive (r,w)

    Returns:
        returns instance of `dotcati.ArchiveModel.BaseArchive` as loaded package object
    """
    if os.path.isfile(file_path):
        if mimetypes.guess_type(file_path)[0] == 'application/x-debian-package':
            # package is a deb package
            # convert deb2cati
            file_path = PkgConvertor.deb2cati(file_path)
        elif mimetypes.guess_type(file_path)[0] == 'application/x-redhat-package-manager':
            # package is a rpm package
            # convert rpm2cati
            file_path = PkgConvertor.rpm2cati(file_path)

    # open v1 as default
    pkg = ArchiveModelV1(file_path, type_str)
    if pkg.pkg_version() == '1.0':
        return ArchiveModelV1(file_path, type_str)
    # return v1 object by default
    return ArchiveModelV1(file_path, type_str)

class ArchiveModelV1(BaseArchive):
    """ .cati package file model (v1.0) """
    pass
