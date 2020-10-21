#
# BaseTransaction.py
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

''' Transaction base model '''

from package.Pkg import Pkg
from frontend import Env

class BaseTransaction:
    ''' Transaction base model '''
    @staticmethod
    def handle_state(section: str, pkg: Pkg):
        """ add new item to state """
        f = open(Env.state_file(), 'r')
        current_content = f.read()
        current_content += section + '%' + pkg.data['name'] + '%' + pkg.data['version'] + '%' + pkg.data['arch'] + '\n'
        f.close()
        f = open(Env.state_file(), 'w')
        f.write(current_content)
        f.close()

    @staticmethod
    def finish_last_state():
        """ set last item in state to finished """
        f = open(Env.state_file(), 'r')
        current_content = f.read()
        current_content = current_content[:len(current_content)-1]
        current_content += '@\n'
        f.close()
        f = open(Env.state_file(), 'w')
        f.write(current_content)
        f.close()

    @staticmethod
    def finish_all_state():
        """ clear all of states """
        f = open(Env.state_file(), 'w')
        f.write('')
        f.close()
