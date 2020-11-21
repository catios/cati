#
# UpdateCommand.py
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

""" Update command """

import time
import random
import json
from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi
from cmdline.components import ReposListErrorShower
from repo.Repo import Repo
from frontend import Env, RootRequired
from dotcati.PackageJsonValidator import PackageJsonValidator

class UpdateCommand(BaseCommand):
    """ Update command """
    def help(self):
        """
        updates list of available packages from repositories

        Usage: cati update [options]
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'finfo',
            'options': {
                '--quiet': [False, False],
                '-q': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def run(self):
        """ Run command """

        RootRequired.require_root_permission()

        if not self.is_quiet():
            pr.p('Loading repositories list...')
        repos = Repo.get_list()
        ReposListErrorShower.show(repos)

        if not self.is_quiet():
            pr.p('Prepairing to update repos...')
        orig_repos = []
        for repo in repos:
            if repo.successful_loaded:
                if repo.test():
                    orig_repos.append(repo)

        if not self.is_quiet():
            pr.p('Updating repositories...')
            pr.p('=============================')

        # downloaded repos data files paths
        downloaded_paths = []

        # update repos
        for repo in orig_repos:
            if not self.is_quiet():
                pr.p('Fetching ' + repo.name + ' (' + repo.url + ') data...')
            data = repo.get_data()
            if type(data) == int:
                pr.e(ansi.red + 'Cannot update ' + repo.name + ' (' + repo.url + '): error code ' + str(data) + ansi.reset)
                pass
            else:
                # validate data
                try:
                    tmp = json.loads(data)
                    # save data in an file
                    path = Env.cache_dir('/' + repo.name + '-' + str(time.time()) + str(random.random())) + '.json'
                    f = open(path, 'w')
                    f.write(data)
                    f.close()
                    downloaded_paths.append(path)
                except:
                    raise
                    pr.e(ansi.red + 'Cannot update ' + repo.name + ' (' + repo.url + '): invalid json data recived' + ansi.reset)

        # load downloaded data
        packages = []
        for path in downloaded_paths:
            f = open(path, 'r')
            data = f.read().strip()
            f.close()
            items = json.loads(data)
            for item in items:
                if PackageJsonValidator.validate(item):
                    packages.append(item)
                else:
                    # TODO : show error
                    pass

        print(packages)
