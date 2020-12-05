#
# TestCore.py
#
# the cati project
# Copyright 2020 parsa shahmaleki <parsampsh@gmail.com>
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

""" Testing system core """

import os
import shutil
from cmdline.kernel import commands
from cmdline import ArgParser
from frontend import Env, HealthChecker

class TestCore:
    """ Testing system core """
    def __init__(self):
        self.raising = True

    def get_name(self):
        """ Returns test name """
        str_type = str(type(self))
        str_type = str_type[14:]
        str_type = str_type[:len(str_type)-2]
        str_type = str_type[:int(len(str_type)/2)]
        return str_type

    def do_assert(self, value, error_msg=''):
        try:
            assert value
        except:
            if self.raising:
                print('Assertion Error: ' + error_msg)
            raise

    def disable_raising(self):
        """ Disable assert error raising """
        self.raising = False

    def enable_raising(self):
        """ Enable assert error raising """
        self.raising = True

    def assert_true(self, value):
        """ Assert True """
        self.do_assert(value, 'asserting that false is true')

    def run_command(self, command_name: str, arguments=[]):
        """ Runs cmdline command """
        arguments.insert(0, 'cati')
        arguments.insert(1, command_name)
        cmd = commands[command_name]()
        out = cmd.handle(ArgParser.parse(arguments))
        if out == None:
            out = 0
        return int(out)

    def assert_equals(self, first_value, last_value):
        self.do_assert(
            first_value == last_value,
            'asserting "' + str(first_value) + '" equals "' + str(last_value) + '"'
        )

    def env(self, path=''):
        return Env.base_path(path)

    def refresh_env(self):
        """ Clear all of effects on testing environment """
        for item in os.listdir(self.env()):
            if os.path.isfile(self.env('/' + item)):
                os.remove(self.env('/' + item))
            else:
                shutil.rmtree(self.env('/' + item))

        # repair cati installation
        HealthChecker.check({})
