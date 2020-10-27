#
# HelpCommand.py
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

''' Help command '''

from cmdline.BaseCommand import BaseCommand
from cmdline import kernel, ansi, pr
from frontend.Version import version as cati_version

class HelpCommand(BaseCommand):
    def help(self):
        '''
        shows this help
        '''
        pass

    def define(self) -> dict:
        ''' Define and config this command '''
        return {
            'name': 'help',
            'options': {
                '-v': [False, False], # [is-required, can-get-value]
                '--version': [False, False]
            },
            'max_args_count': 1,
            'min_args_count': 0,
        }

    def run(self):
        ''' Run command '''

        # check -v|--version options
        if self.has_option('--version') or self.has_option('-v'):
            pr.p(cati_version)
            return

        pr.p(ansi.cyan + "  ______               __      __ ")
        pr.p(ansi.cyan + " /      \             /  |    /  |")
        pr.p(ansi.cyan + "//" + ansi.yellow + "$$$$$$" +ansi.cyan + "  |  ______   _" + ansi.yellow + "$$" + ansi.cyan + " |_   " + ansi.yellow + "$$"+ansi.cyan +"/ ")
        pr.p(ansi.yellow + "$$" + ansi.cyan + " |  " + ansi.yellow + "$$"  + ansi.cyan + "/  /      \ / " + ansi.yellow + "$$" + ansi.cyan + "   |  /  |")
        pr.p(ansi.yellow + "$$" + ansi.cyan + " |       " + ansi.yellow + "$$$$$$" + ansi.cyan + "  |" + ansi.yellow + "$$$$$$"   + ansi.cyan + "/   " + ansi.yellow + "$$"  + ansi.cyan +" |")
        pr.p(ansi.yellow + "$$" + ansi.cyan + " |   __  /    " + ansi.yellow +  "$$" + ansi.cyan + " |  " + ansi.yellow +  "$$" + ansi.cyan + " | __ "  + ansi.yellow +  "$$" + ansi.cyan + " |")
        pr.p(ansi.yellow + "$$" + ansi.cyan + " \__/  |/" + ansi.yellow + "$$$$$$$" + ansi.cyan + " |  " + ansi.yellow + "$$" + ansi.cyan + " |/  |" + ansi.yellow + "$$" + ansi.cyan + " | " + self.general_help().split('\n')[0])
        pr.p(ansi.yellow + "$$    $$" + ansi.cyan + "/" +ansi.yellow+ " $$    $$ " + ansi.cyan + "|" + ansi.yellow + "  $$  $$" + ansi.cyan + "/"+ansi.yellow+" $$" + ansi.cyan + " | " + self.general_help().split('\n')[1])
        pr.p(ansi.yellow + " $$$$$$" + ansi.cyan + "/" + ansi.yellow + "   $$$$$$$" + ansi.cyan +"/" + ansi.yellow + "    $$$$" + ansi.cyan + "/" + ansi.yellow + "  $$" + ansi.cyan + "/ " + ansi.cyan + " " + self.general_help().split('\n')[2] + ansi.reset)

        pr.p('\nOptions:')
        pr.p('\t-v|--version: shows cati version')
        pr.p('\t--no-ansi: disable terminal ansi colors')
        pr.p('\t--help: pass it to commands to show help of that command')

        pr.p()

        commands = kernel.commands

        # check arguments
        if len(self.arguments) >= 1:
            # a command inserted. show detail of that command
            try:

                cmd = commands[self.arguments[0]]
                obj = cmd()
                pr.p(obj.help_full(False))
                return 0
            except:
                self.message('unknow command "' + self.arguments[0] + '"' + ansi.reset, True, before=ansi.red)
                return 1

        # show summary help of command
        pr.p('Subcommands:')
        for cmd in commands:
            obj = commands[cmd]()
            pr.p('\t' + ansi.green + cmd + ansi.reset + '\t' + obj.help_summary())

        pr.p('\nfor see detailed help about commands, run: "' + ansi.yellow + self.cati_exec + ' help [command-name]' + ansi.reset + '"')

        return 0
