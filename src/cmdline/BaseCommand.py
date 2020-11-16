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

""" Cmdline command model base """

import sys
from cmdline import pr
from frontend.Version import version as cati_version
from cmdline.commands import HelpCommand
from cmdline import ArgParser

class BaseCommand:
    """ Cmdline command model base """

    def validate(self, args: dict):
        """
        Validate inserted arguments in command config frame
        loads command config from `config` function output
        next checks arguments and compares them with command config
        then, if an unknow option is inserted or more/less argument inserted,
        shows error to user
        """

        # load command config
        command_config = self.config()
        # add --help option as default
        command_config['options']['--help'] = [False, False]

        self.name = command_config['name']
        self.cati_exec = sys.argv[0]

        # pop first argument (command self name)
        args['arguments'].pop(0)

        # check knowed options and value of them
        for k in args['options']:
            try:
                option_config = command_config['options'][k]
            except:
                self.message('unknow option "' + k + '"')
                return pr.exit(1)

            if option_config[1] == True:
                if args['options'][k] == None:
                    self.message('option ' + k + ' requires value')
                    return pr.exit(1)

        # check required options
        for option in command_config['options']:
            if command_config['options'][option][0] == True:
                try:
                    args['options'][option]
                except:
                    self.message('option ' + option + ' is required')
                    return pr.exit(1)

        self.args = args
        self.arguments = self.args['arguments']

        # check arguments count
        if not self.has_option('--help'):
            if command_config['max_args_count'] != None:
                if len(args['arguments']) > command_config['max_args_count']:
                    self.message('this command requires less than ' + str(command_config['max_args_count']+1) + ' arguments')
                    return pr.exit(1)

            if command_config['min_args_count'] != None:
                if len(args['arguments']) < command_config['min_args_count']:
                    self.message('this command requires more than ' + str(command_config['min_args_count']-1) + ' arguments')
                    return pr.exit(1)

    def handle(self, args: dict):
        """
        Handle run the command
        first, validates arguments
        next, checks if --help inserted, show command help
        if not, run command
        """
        self.validate(args)

        # handle --help option
        if self.has_option('--help'):
            help_cmd = HelpCommand.HelpCommand()
            return help_cmd.handle(ArgParser.parse(['cati', 'help', self.name]))

        return self.run()

    def has_option(self, option: str):
        """
        Checks the option is inserted
        """
        try:
            self.args['options'][option]
            return True
        except:
            return False

    def option_value(self, option: str):
        """
        Returns value of option
        """
        if not self.has_option(option):
            # if option not inserted, return None as default
            return None

        return self.args['options'][option]

    def message(self, msg, is_error=False, before=''):
        """
        Prints a message like this:
        cati: <command-name>: <the-message>

        arguments:
        - `is_error`: if this is True, message will print on stderr
        - `before`: before will print in the first of message
        """
        msg = before + self.cati_exec + ': ' + self.name + ': ' + msg

        if is_error:
            pr.e(msg)
        else:
            pr.p(msg)

    def general_help(self):
        """
        returns general help of cati cli
        """
        return """Cati package manager [""" + cati_version + """]
Copyright 2020 parsa mpsh - GPL-3
Usage: cati [command] [options] [args]"""

    def help_full(self, with_general_help=True):
        """
        Returns full help of command
        the `with_general_help` argument used to include/exclude general help of cati
        """
        help_text = self.help.__doc__
        help_text = help_text.strip()
        help_text_tmp = ''
        for line in help_text.split('\n'):
            line = line.strip()
            help_text_tmp += line + '\n'

        help_text = help_text_tmp.strip()

        if with_general_help:
            help_text = self.general_help() + '\n\n' + help_text

        return help_text

    def help_summary(self):
        """ Returns summary of help (first line only) """
        return self.help_full(False).split('\n')[0]

    def is_quiet(self):
        """ Checks --quiet and -q options """
        return self.has_option('-q') or self.has_option('--quiet')

    def is_verbose(self):
        """ Checks --verbose and -v options """
        return self.has_option('-v') or self.has_option('--verbose')
