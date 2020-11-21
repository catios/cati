#
# Http.py
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

""" repo http driver """

import requests
from repo.drivers.BaseDriver import BaseDriver

class Http(BaseDriver):
    """ repo http driver """
    def test(self):
        """ test repo """
        try:
            res = requests.get(self.url + '?cati-repo-test=1')
        except:
            return False
        return res.ok

    def get_data(self):
        """ Returns repo data """
        res = requests.get(self.url + '?get_data=1')
        if not res.ok:
            return int(res.status_code)
        return res.text
