#
# FullUpgradeCommand.py
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

""" FullUpgrade command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import ArgParser
from .AutoremoveCommand import AutoremoveCommand
from .UpdateCommand import UpdateCommand
from .UpgradeCommand import UpgradeCommand

class FullUpgradeCommand(BaseCommand):
    """ FullUpgrade command """
    def help(self):
        """
        update, upgrade and autoremove

        Usage: cati full-upgrade [options]

        Options:
        -y|--yes: don't ask for user confirmation
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'full-upgrade',
            'options': {
                '-y': [False, False],
                '--yes': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """

        options = []
        if self.has_option('-y') or self.has_option('--yes'):
            options = ['-y']

        update_cmd = UpdateCommand()
        res = update_cmd.handle(ArgParser.parse(['cati', 'update']))
        if res != 0 and res != None:
            return res

        upgrade_cmd = UpgradeCommand()
        res = upgrade_cmd.handle(ArgParser.parse(['cati', 'upgrade', *options]))
        if res != 0 and res != None:
            return res

        autoremove_cmd = AutoremoveCommand()
        res = autoremove_cmd.handle(ArgParser.parse(['cati', 'autoremove', *options]))
        if res != 0 and res != None:
            return res
