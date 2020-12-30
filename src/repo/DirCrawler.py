#
# DirCrawler.py
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

""" Crawls an directory and extracts packages data from that """

import os
import json

class DirCrawler:
    """ Crawls an directory and extracts packages data from that """
    def __init__(self, dirpath: str):
        self.dirpath = dirpath
        self.loaded_packages = []

    def add_once(self, path: str):
        """
        add once package data item
        
        Args:
            path (str): package filepath
        """
        if path.split('.')[-1] != 'json':
            return
        try:
            f = open(path, 'r')
            content = f.read()
            f.close()
            json_data = json.loads(content.strip())
        except:
            return
        # add item
        self.loaded_packages.append(json_data)

    def start(self, path=''):
        """
        start crwaling (loaded packages will put in self.loaded_packages)
        
        Args:
            path (str): directory path
        """
        if path == '':
            path = self.dirpath
        for item in os.listdir(path):
            if os.path.isdir(path + '/' + item):
                self.start(path + '/' + item)
            else:
                self.add_once(path + '/' + item)
