#
# RepoCommand.py
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

""" Repo command """

import os
from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.repo.Repo import Repo
from cati.repo import Scanner
from cati.cmdline.components import ReposListErrorShower
from cati.frontend import Env, RootRequired

class RepoCommand(BaseCommand):
    """ Repo command """
    def help(self):
        """
        manage repositories

        Usage: cati repos [options]

        Options:
        -e|--edit: open repositories config file with editor
        -a|--add [new-repo]: add new repository
        --scan [directory]: scans packages inside in a directory and creates data files for repo
        -q|--quiet: quiet output

        Repo config structure:
        <url> pkg=<type(s) of packages. for example `cati` or `deb`> arch=<wanted architecture> channel=<wanted version channel(s)> name=<an name for repo> priority=<priority between another repos>
        
        Example:
        https://pkg.example.com/packages pkg=cati arch=all,i386 name=main-repo
        file:///path/to/packages pkg=cati,deb arch=all channel=alpha,security name=deb-repo
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'repo',
            'options': {
                '-q': [False, False],
                '--quiet': [False, False],
                '--edit': [False, False],
                '-e': [False, False],
                '--add': [False, False],
                '-a': [False, False],
                '--scan': [False, False],
            },
            'max_args_count': None,
            'min_args_count': None,
        }

    def run(self):
        """ Run command """

        if self.has_option('--edit') or self.has_option('-e'):
            return os.system('vim "' + Env.repos_config() + '"')

        if self.has_option('--add') or self.has_option('-a'):
            RootRequired.require_root_permission()
            repo_string = ''
            for arg in self.arguments:
                repo_string += arg + ' '
            repo_string = repo_string.strip()
            tmp_repo = Repo(repo_string)
            tmp_repo.loaded_from_file = 'argument'
            tmp_repo.line_number = 0
            if not tmp_repo.successful_loaded:
                ReposListErrorShower.show([tmp_repo])
                return 1
            # write repo
            path = Env.repos_config_dir('/' + tmp_repo.name + '-' + tmp_repo.get_pkg_str() + '-' + tmp_repo.get_arch_str())
            tmp = ''
            tmp_i = 1
            while os.path.isfile(path + tmp):
                tmp = '-' + str(tmp_i)
            f = open(path, 'w')
            f.write('# added manually\n' + repo_string)
            f.close()
            return 0

        if self.has_option('--scan'):
            for arg in self.arguments:
                if os.path.isdir(arg):
                    Scanner.scan(arg)
                    pr.p(ansi.green + 'directory ' + arg + ' scanned successfully' + ansi.reset)
                else:
                    self.message('directory' + arg + ' not found', is_error=True)
            return 0

        # show list of repos
        if not self.is_quiet():
            pr.p('Loading repositories list...')
        repos = Repo.get_list()
        if not self.is_quiet():
            pr.p('============================')
        ReposListErrorShower.show(repos)
        for repo in repos:
            if repo.successful_loaded:
                is_disable = ''
                if repo.is_disable:
                    is_disable = ' (Disabled)'
                pr.p(repo.name + ': ' + repo.url + ' pkg=' + repo.get_pkg_str() + ' arch=' + repo.get_arch_str() + ' channel=' + repo.get_channel_str() + is_disable)
