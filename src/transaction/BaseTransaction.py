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

"""
Transaction base model.

transactions are install/remove/upgrade/downgrade operations.
"""

from package.Pkg import Pkg
from frontend import Env
from transaction.Calculator import Calculator

class BaseTransaction:
    """ Transaction base model """

    @staticmethod
    def finish_all_state():
        """ clear all of states """
        f = open(Env.state_file(), 'w')
        f.write('')
        f.close()

    @staticmethod
    def add_to_state(calc: Calculator):
        """ add new item to state """
        content = ''
        for item in calc.get_sorted_list():
            content += item['action'] + '%' + item['pkg'].data['name'] + '%' + item['pkg'].data['version'] + '%' + item['pkg'].data['arch'] + '\n'
        f = open(Env.state_file(), 'w')
        f.write(content)
        f.close()

    @staticmethod
    def pop_state():
        """ remove first item from state """
        f = open(Env.state_file(), 'r')
        content = f.read()
        f.close()
        content = content.strip()
        lines = content.split('\n')
        if lines:
            lines.pop(0)
        new_content = ''
        for line in lines:
            new_content += line + '\n'
        f = open(Env.state_file(), 'w')
        f.write(new_content)
        f.close()

    @staticmethod
    def state_item_to_string(state_item: dict) -> str:
        """
        Gets an dictonary as a item in state list where returned by `BaseTransaction.state_list()`
        and generates an human readable message as string to show that message to user
        """
        msg = state_item['action'] + ' ' + state_item['pkg']
        if state_item['version'] == None:
            return msg
        msg += '=' + state_item['version']
        if state_item['arch'] == None:
            return msg
        msg += '=' + state_item['arch']
        return msg

    @staticmethod
    def state_list():
        """ returns list of undoned transactions from state file """
        f = open(Env.state_file(), 'r')
        content = f.read()
        f.close()
        content = content.strip().split('\n')
        content = [line.strip() for line in content]
        result = []
        for item in content:
            if item != '':
                tmp = {}
                parts = item.split('%')
                tmp['action'] = parts[0]
                tmp['pkg'] = parts[1]
                try:
                    tmp['version'] = parts[2]
                except:
                    tmp['version'] = None
                try:
                    tmp['arch'] = parts[3]
                except:
                    tmp['arch'] = None
                result.append(tmp)
        return result
