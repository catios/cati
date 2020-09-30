#
# BaseCommand.py
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

''' Cmdline command model base '''

import sys
from cmdline import pr

class BaseCommand:
    ''' Cmdline command model base '''

    def validate(self , args: dict):
        '''
        Validate inserted arguments in command config frame
        '''

        command_config = self.define()

        self.name = command_config['name']
        self.cati_exec = sys.argv[0]

        args['arguments'].pop(0)

        # check knowd options and value of them
        for k in args['options']:
            try:
                option_config = command_config['options'][k]
            except:
                self.message('unknow option "' + k + '"')
                pr.exit(1)

            if option_config[1] == True:
                if args['options'][k] == None:
                    self.message('option ' + k + ' requires value')
                    pr.exit(1)

        # check required options
        for option in command_config['options']:
            if command_config['options'][option][0] == True:
                try:
                    args['options'][option]
                except:
                    self.message('option ' + option + ' is required')
                    pr.exit(1)

        # check arguments count
        if len(args['arguments']) > command_config['max_args_count']:
            self.message('this command requires less than ' + str(command_config['max_args_count']+1) + ' arguments')
            pr.exit(1)

        if len(args['arguments']) < command_config['min_args_count']:
            self.message('this command requires more than ' + str(command_config['min_args_count']-1) + ' arguments')
            pr.exit(1)

        # everything is ok, run command
        self.args = args

    def handle(self , args: dict):
        ''' Handle run the command '''
        self.validate(args)
        return self.run()

    def has_option(self , option: str):
        ''' Checks the option is inserted '''
        try:
            self.args['options'][option]
            return True
        except:
            return False

    def option_value(self , option: str):
        ''' Returns value of option '''
        if not self.has_option(option):
            return None
        
        return self.args['options'][option]

    def message(self , msg , is_error=False):
        ''' Prints a message on screen '''
        msg = self.cati_exec + ': ' + self.name + ': ' + msg

        if is_error:
            pr.e(msg)
        else:
            pr.p(msg)
