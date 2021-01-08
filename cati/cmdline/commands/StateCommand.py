#
# StateCommand.py
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

""" State command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.cmdline.components import StateContentShower
from .RemoveCommand import RemoveCommand
from .PkgCommand import PkgCommand
from cati.cmdline import ArgParser
from cati.transaction.BaseTransaction import BaseTransaction
from cati.frontend.RootRequired import require_root_permission
from cati.dotcati.ArchiveModel import archive_factory

class StateCommand(BaseCommand):
    """ State command """
    def help(self):
        """
        manage transactions state

        Usage: cati state [options]
        
        Options:
        --abort: cancel undoned transactions
        --complete: complete undoned transactions
        -y|--yes: do not ask for user confirmation
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'state',
            'options': {
                '--abort': [False, False],
                '--complete': [False, False],
                '--yes': [False, False],
                '-y': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """

        if self.has_option('--abort'):
            require_root_permission()
            state_list = BaseTransaction.state_list()
            if not state_list:
                pr.p(ansi.green + 'There is not any undoned transaction and everything is ok' + ansi.reset)
                return 0
            user_answer = 'y'
            if not self.has_option('-y') and not self.has_option('--yes'):
                pr.p(ansi.yellow + 'WARNING: this process maybe dangerous and ' + str(len(state_list)) + ' transactions will be igonred. are you sure? [y/N] ' + ansi.reset, end='')
                user_answer = input()
            if user_answer in ['Y', 'y']:
                BaseTransaction.finish_all_state()
                pr.p(ansi.green + 'state was empty successfully' + ansi.reset)
            else:
                return
        elif self.has_option('--complete'):
            require_root_permission()
            state_list = BaseTransaction.state_list()
            if not state_list:
                pr.p(ansi.green + 'There is not any undoned transaction and everything is ok' + ansi.reset)
                return 0
            BaseTransaction.finish_all_state()
            # complete transactions
            for item in state_list:
                if item['action'] == 'remove':
                    tmp_arguments = [item['pkg'], '-y']
                    tmp_arguments.insert(0, 'cati')
                    tmp_arguments.insert(1, 'remove')
                    cmd = RemoveCommand()
                    cmd.handle(ArgParser.parse(tmp_arguments))
                elif item['action'] == 'install':
                    tmp_arguments = ['install', item['file']]
                    tmp_arguments.insert(0, 'cati')
                    tmp_arguments.insert(1, 'pkg')
                    cmd = PkgCommand()
                    cmd.handle(ArgParser.parse(tmp_arguments))
            return
        else:
            # show list of undoned transactions
            state_list = BaseTransaction.state_list()
            if state_list:
                StateContentShower.show(state_list)
                return 1
            else:
                pr.p(ansi.green + 'There is not any undoned transaction and everything is ok' + ansi.reset)
                return 0
