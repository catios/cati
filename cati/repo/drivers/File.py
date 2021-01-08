#
# File.py
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

""" repo file driver """

import os
import json
from cati.repo.drivers.BaseDriver import BaseDriver
from cati.repo.DirCrawler import DirCrawler

class File(BaseDriver):
    """ repo file driver """
    def test(self) -> bool:
        """ test repo """
        dir_path = self.url.split('://', 1)[-1]
        return os.path.isdir(dir_path) and os.access(dir_path, os.R_OK)

    def get_data(self, download_event=None) -> str:
        """ Returns repo data """
        crawler = DirCrawler(self.url.split('://', 1)[-1])
        crawler.start()
        try:
            return json.dumps(crawler.loaded_packages)
        except:
            return '[]'
