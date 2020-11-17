#
# CheckCommand.py
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

""" Check command """

import os
from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi, ArgParser
from frontend.RootRequired import require_root_permission
from cmdline.commands.StateCommand import StateCommand
from package.Pkg import Pkg
from helpers.hash import calc_file_sha256
from frontend import Env

class CheckCommand(BaseCommand):
    """ Check command """
    def help(self):
        """
        checks system health and security

        this command checks system health and packages security and static files
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'check',
            'options': {
                '--quiet': [False, False],
                '-q': [False, False],
                '--verbose': [False, False],
                '-v': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """
        
        # require root permission
        require_root_permission()

        if not self.is_quiet():
            pr.p('Starting checking system health and security...')
            pr.p('===============================================')

        # check state
        state_cmd = StateCommand()
        out = state_cmd.handle(ArgParser.parse(['cati', 'state']))
        if out > 0:
            return out

        # search for conflict and dependency corruptions
        if not self.is_quiet():
            pr.p('Checking dependency and conflict corruptions...')
        dependency_problems = []
        conflict_problems = []
        installed_packages = Pkg.installed_list()['list']
        for pkg in installed_packages:
            if self.is_verbose():
                pr.p('[info] checking dependencies and conflicts for ' + pkg.data['name'] + '...')
            for dp in pkg.get_depends():
                if not Pkg.check_state(dp):
                    dependency_problems.append([
                        [pkg, dp]
                    ])
            for conflict in pkg.get_conflicts():
                if Pkg.check_state(conflict):
                    conflict_problems.append([
                        [pkg, conflict]
                    ])

        if dependency_problems or conflict_problems:
            for depend in dependency_problems:
                pr.p(ansi.red + 'dependency problem for ' + depend[0].data['name'] + ': ' + depend[1] + ansi.reset)
            for conflict in conflict_problems:
                pr.p(ansi.red + 'conflict problem for ' + conflict[0].data['name'] + ': ' + conflict[1] + ansi.reset)
            return 1
        else:
            pr.p(ansi.green + 'There is not any conflict or dependnecy problem and everything is ok' + ansi.reset)

        # check static files
        if not self.is_quiet():
            pr.p('Checking packages static files...')
        staticfile_problems = []
        for pkg in installed_packages:
            if self.is_verbose():
                pr.p('[info] checking static files for ' + pkg.data['name'] + '...')
            files = pkg.installed_static_files()
            for f in files:
                f[1] = Env.base_path(f[1])
                if os.path.isfile(f[1]):
                    wanted_hash = f[0]
                    current_hash = calc_file_sha256(f[1])
                    if wanted_hash != current_hash:
                        staticfile_problems.append([
                            pkg,
                            f,
                            'file is changed'
                        ])
                else:
                    staticfile_problems.append([
                        pkg,
                        f,
                        'file is deleted'
                    ])
        if staticfile_problems:
            for problem in staticfile_problems:
                pr.p(ansi.red + 'staticfile problem in package ' + problem[0].data['name'] + ': ' + problem[1][1] + ': ' + problem[2])
            return 1
        else:
            pr.p(ansi.green + 'all of static files are ok' + ansi.reset)
        
        # TODO : check database and configuration files health
