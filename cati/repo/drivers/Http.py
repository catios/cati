#
# Http.py
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

""" repo http driver """

import os
import requests
from cati.repo.drivers.BaseDriver import BaseDriver
from cati.frontend import Temp

class Http(BaseDriver):
    """ repo http driver """
    def test(self) -> bool:
        """ test repo """
        try:
            res = requests.get(self.url + '?cati-repo-test=1')
        except:
            return False
        return res.ok

    def get_data(self, download_event=None) -> str:
        """ Returns repo data """
        i = 0
        last_res = None
        temp_file = Temp.make_file()
        os.remove(temp_file)
        while i < 5:
            if i > 4:
                return last_res
            last_res = download_event(self.url + '?get_data=1', temp_file)
            if last_res == True:
                f = open(temp_file, 'r')
                content = f.read().strip()
                f.close()
                if content != '':
                    return content
            i += 1
