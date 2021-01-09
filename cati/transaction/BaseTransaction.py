#
# BaseTransaction.py
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
Transaction base model.

transactions are install/remove/upgrade/downgrade operations.
"""

import os
from cati.dotcati.Pkg import Pkg
from cati.frontend import Env
from .Calculator import Calculator

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
        if state_item['file'] == None:
            return msg
        msg += ' (' + state_item['file'] + ')'
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
                try:
                    tmp['file'] = parts[4]
                except:
                    tmp['file'] = None
                result.append(tmp)
        return result

    @staticmethod
    def run_any_scripts(runed_transactions: list, events: dict):
        """
        run all of `any` scripts.
        
        events:
        - start_run_script: will run when starting to run once script (gets package name)
        """
        runed_transactions_str = ''
        for rt in runed_transactions[1]:
            runed_transactions_str += rt + ' '
        runed_transactions_str = runed_transactions_str.strip()
        scripts = os.listdir(Env.any_scripts())
        for script in scripts:
            events['start_run_script'](script)
            # run script
            os.system('chmod +x "' + Env.any_scripts('/' + script) + '"')
            os.system(Env.any_scripts('/' + script) + ' ' + runed_transactions[0] + ' ' + runed_transactions_str)
