#
# SecurityBlacklist.py
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

"""
Cati has a feature to block malware packages (detected)
this feature is a database from sha256, md5 and sha512 hashes
this database declares the malware packages.
cati checks packages hashes and checks them in this database.
if package is in database, will not install and user will get error
"this package is a malware" and details of database
"""

import os
import json
from . import Env

def get_list() -> list:
    """
    returns list of blaclist items
    
    Returns:
        list: returns list of blacklist items
    """
    db_parts = os.listdir(Env.security_blacklist())
    blacklist = []
    for part in db_parts:
        try:
            f = open(Env.security_blacklist('/' + part), 'r')
            content = f.read()
            content = json.loads(content)
            f.close()
        except:
            continue
        for item in content:
            try:
                assert type(item['title']) == str
                assert type(item['description']) == str
                assert type(item['md5']) == str
                assert type(item['sha256']) == str
                assert type(item['sha512']) == str
                blacklist.append(item)
            except:
                pass
    return blacklist
