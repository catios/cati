#
# Remove.py
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

''' Remove transaction '''

from transaction.BaseTransaction import BaseTransaction
from package.Pkg import Pkg

class Remove(BaseTransaction):
    ''' Remove transaction '''
    @staticmethod
    def run(pkg: Pkg, events: dict):
        ''' Remove pkg '''
        BaseTransaction.handle_state('remove', pkg)

        events['removing_package'](pkg)

        # remove package

        events['package_remove_finished'](pkg)

        BaseTransaction.finish_last_state()
