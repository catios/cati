#
# ClearCacheCommand.py
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

""" ClearCache command """

import os
from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.frontend import Env, RootRequired

class ClearCacheCommand(BaseCommand):
    """ ClearCache command """
    def help(self):
        """
        clears cache files

        Usage: sudo cati clear-cache [options]

        Options:
        -v|--verbose: verbose output
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'clear-cache',
            'options': {
                '-v': [False, False],
                '--verbose': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """

        RootRequired.require_root_permission()

        for f in os.listdir(Env.cache_dir()):
            if os.path.isfile(Env.cache_dir('/' + f)):
                if self.is_verbose():
                    pr.p('removing ' + Env.cache_dir('/' + f) + '...')
                os.remove(Env.cache_dir('/' + f))
        for f in os.listdir(Env.cache_dir('/archives')):
            if os.path.isfile(Env.cache_dir('/archives/' + f)):
                if self.is_verbose():
                    pr.p('removing ' + Env.cache_dir('/archives/' + f) + '...')
                os.remove(Env.cache_dir('/archives/' + f))

        pr.p(ansi.green + 'Cache files cleared successfully' + ansi.reset)
