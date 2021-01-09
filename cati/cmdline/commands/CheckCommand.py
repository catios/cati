#
# CheckCommand.py
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

""" Check command """

import os
import json
from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi, ArgParser
from cati.frontend.RootRequired import require_root_permission
from .StateCommand import StateCommand
from .InstallCommand import InstallCommand
from cati.cmdline.components import ReposListErrorShower
from cati.dotcati.Pkg import Pkg
from cati.helpers.hash import calc_file_sha256
from cati.frontend import Env
from cati.repo.Repo import Repo

class CheckCommand(BaseCommand):
    """ Check command """
    def help(self):
        """
        checks system health and security

        this command checks system health and packages security and static files

        Usage: sudo cati check [options]

        Options:
        -q|--quiet: quiet output
        -v|--verbose: verbose output
        --autofix: automatically fix problems by re-installing some packages
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
                '--autofix': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """
        
        # require root permission
        require_root_permission()

        result_code = 0

        packages_to_reinstall = []

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
                        pkg, dp
                    ])
            for conflict in pkg.get_conflicts():
                if Pkg.check_state(conflict):
                    conflict_problems.append([
                        pkg, conflict
                    ])

        if dependency_problems or conflict_problems:
            for depend in dependency_problems:
                pr.p(ansi.red + 'dependency problem for ' + depend[0].data['name'] + ': ' + depend[1] + ansi.reset)
                packages_to_reinstall.append(depend[0])
            for conflict in conflict_problems:
                pr.p(ansi.red + 'conflict problem for ' + conflict[0].data['name'] + ': ' + conflict[1] + ansi.reset)
                packages_to_reinstall.append(conflict[0])
            result_code = 1
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
                pr.p(ansi.red + 'staticfile problem in package ' + problem[0].data['name'] + ': ' + problem[1][1] + ': ' + problem[2] + ansi.reset)
                packages_to_reinstall.append(problem[0])
            result_code = 1
        else:
            pr.p(ansi.green + 'all of static files are ok' + ansi.reset)
        
        # check repos config files health
        if not self.is_quiet():
            pr.p('Checking cati configuration files...')
        if self.is_verbose():
                pr.p('[info] checking repositories config...')
        repos = Repo.get_list()
        pr.p(ansi.red, end='')
        ReposListErrorShower.show(repos)
        pr.p(ansi.reset, end='')
        is_any_repo_error = False
        for repo in repos:
            if repo.syntax_errors:
                is_any_repo_error = True
                result_code = 1
        if not is_any_repo_error:
            pr.p(ansi.green + 'all of cati configuration files are ok' + ansi.reset)

        # check database files
        if not self.is_quiet():
            pr.p('Checking cati database...')
        database_problems = []
        for f in os.listdir(Env.installed_lists()):
            if self.is_verbose():
                pr.p('[info] checking database install dir for ' + f + '...')
            if not os.path.isfile(Env.installed_lists('/' + f + '/files')) or not os.path.isfile(Env.installed_lists('/' + f + '/ver')):
                database_problems.append('installed packages database: directory ' + Env.installed_lists('/' + f) + ' is corrupt')
        for f in os.listdir(Env.security_blacklist()):
            if self.is_verbose():
                pr.p('[info] checking security blacklist part ' + f + '...')
            if not os.path.isfile(Env.security_blacklist('/' + f)):
                database_problems.append('security blacklist: an directory detected: ' + Env.security_blacklist('/' + f))
            else:
                tmp = open(Env.security_blacklist('/' + f), 'r')
                try:
                    json.loads(tmp.read())
                except:
                    database_problems.append('security blacklist: invalid json data in ' + Env.security_blacklist('/' + f))
        if database_problems:
            for problem in database_problems:
                pr.p(ansi.red + 'database: ' + problem + ansi.reset)
            result_code = 1
        else:
            pr.p(ansi.green + 'all of cati database is ok' + ansi.reset)

        if not self.is_quiet():
            if packages_to_reinstall:
                pr.p(ansi.blue + 'We suggest re-install this packages:')
                for pkg in packages_to_reinstall:
                    pr.p('- ' + pkg.data['name'])
                if not self.has_option('--autofix'):
                    pr.p('use --autofix option to re-install them or do this manually')
                    pr.p(ansi.reset, end='')
                else:
                    pr.p(ansi.reset, end='')
                    packages_names = [pkg.data['name'] for pkg in packages_to_reinstall]
                    install_cmd = InstallCommand()
                    args = ['cati', 'install', '--reinstall', *packages_names]
                    cmd_str = ''
                    for arg in args:
                        cmd_str += arg + ' '
                    cmd_str = cmd_str.strip()
                    pr.p(cmd_str)
                    return install_cmd.handle(ArgParser.parse(args))

        return result_code
