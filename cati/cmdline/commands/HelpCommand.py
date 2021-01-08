#
# HelpCommand.py
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

""" Help command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import kernel, ansi, pr
from cati.frontend.Version import version as cati_version

class HelpCommand(BaseCommand):
    """ Help command """
    def help(self):
        """
        shows this help
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'help',
            'options': {
                '-v': [False, False],
                '--version': [False, False],
                '--quiet': [False, False],
                '-q': [False, False],
            },
            'max_args_count': 1,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """

        # check -v|--version options
        if self.has_option('--version') or self.has_option('-v'):
            pr.p(cati_version)
            return

        if not self.is_quiet():
            pr.p()
            pr.p(ansi.yellow + "  $$$$$$                $$     $$" + ansi.reset)
            pr.p(ansi.yellow + " $$    $$              $$" + ansi.reset)
            pr.p(ansi.yellow + " $$         $$$$$$   $$$$$$    $$" + ansi.reset)
            pr.p(ansi.yellow + " $$              $$    $$      $$" + ansi.reset)
            pr.p(ansi.yellow + " $$         $$$$$$$    $$      $$" + ansi.reset + ansi.cyan + " | " + self.general_help().split('\n')[0] + ansi.reset)
            pr.p(ansi.yellow + " $$    $$  $$    $$    $$  $$  $$" + ansi.reset + ansi.cyan + " | " + self.general_help().split('\n')[1] + ansi.reset)
            pr.p(ansi.yellow + "  $$$$$$    $$$$$$$     $$$$   $$" + ansi.reset + ansi.cyan + " | " + self.general_help().split('\n')[2] + ansi.reset)
            pr.p()

        pr.p('Options:')
        pr.p(ansi.header + '\t-v|--version' + ansi.reset + ': shows cati version')
        pr.p(ansi.header + '\t--no-ansi' + ansi.reset + ': disable terminal ansi colors')
        pr.p(ansi.header + '\t--help' + ansi.reset + ': pass it to commands to show help of that command')
        pr.p(ansi.header + '\t-q|--quiet' + ansi.reset + ': quiet output')
        pr.p(ansi.header + '\t-v|--verbose' + ansi.reset + ': verbose output')

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
            tabs = '\t\t'
            if len(cmd) > 7:
                tabs = '\t'
            pr.p('\t' + ansi.green + cmd + ansi.reset + tabs + obj.help_summary())

        if not self.is_quiet():
            pr.p('\nfor see detailed help about commands, run: "' + ansi.yellow + self.cati_exec + ' help [command-name]' + ansi.reset + '"')

        return 0
