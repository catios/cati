#
# UpdateCommand.py
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

""" Update command """

import os
import time
import random
import json
from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.cmdline.components import ReposListErrorShower, DownloadProgress
from cati.repo.Repo import Repo
from cati.frontend import Env, RootRequired
from cati.dotcati.PackageJsonValidator import PackageJsonValidator
from cati.dotcati import ListUpdater
from cati.dotcati.Pkg import Pkg

class UpdateCommand(BaseCommand):
    """ Update command """
    def help(self):
        """
        updates list of available packages from repositories

        Usage: cati update [options]

        Options:
        -q|--quiet: quiet output
        -v|--verbose: verbose output
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'update',
            'options': {
                '--quiet': [False, False],
                '-q': [False, False],
                '--verbose': [False, False],
                '-v': [False, False],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def empty_method(self, a=None, b=None):
        """ an empty method """
        pass

    def download_event(self, url, output):
        """ repo data download event """
        return DownloadProgress.download(url, output)

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
                    if not repo.is_disable:
                        orig_repos.append(repo)
                    else:
                        if not self.is_quiet():
                            self.message('Warning: ignoring repository "' + repo.name + '" because this is disable')
                else:
                    pr.e(ansi.red + 'Cannot make connection to repo "' + repo.full_string + '"' + ansi.reset)

        if not self.is_quiet():
            pr.p('Updating repositories...')
            pr.p('=============================')

        # downloaded repos data files paths
        downloaded_paths = []

        # update repos
        for repo in list(reversed(orig_repos)):
            if not self.is_quiet():
                pr.p('Fetching ' + repo.name + ' (' + repo.url + ') data...')
            data = repo.get_data(download_event=self.download_event)
            if type(data) == int:
                pr.e(ansi.red + 'Cannot update ' + repo.name + ' (' + repo.url + '): error code ' + str(data) + ansi.reset)
            elif isinstance(data, Exception):
                pr.e(ansi.red + 'Cannot update ' + repo.name + ' (' + repo.url + '): ' + str(data) + ansi.reset)
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
                    pr.e(ansi.red + 'Cannot update ' + repo.name + ' (' + repo.url + '): invalid json data recived' + ansi.reset)

        if not self.is_quiet():
            pr.p('Updating packages list...')

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
                    pass

        for pkg in packages:
            if PackageJsonValidator.validate(pkg):
                if self.is_verbose():
                    pr.p('adding ' + pkg['name'] + ':' + pkg['version'] + ':' + pkg['arch'] + '...')
                # write package on list
                if not os.path.isdir(Env.packages_lists('/' + pkg['name'])):
                    os.mkdir(Env.packages_lists('/' + pkg['name']))
                try:
                    f = open(Env.packages_lists('/' + pkg['name'] + '/' + pkg['version'] + '-' + pkg['arch']), 'w')
                    f.write(json.dumps(pkg))
                    f.close()
                    ListUpdater.index_reverse_depends_and_conflicts(Pkg(pkg))
                except:
                    pr.e(ansi.red + 'error while adding ' + pkg['name'] + ':' + pkg['version'] + ':' + pkg['arch'] + ansi.reset)
            else:
                if self.is_verbose():
                    pr.p(ansi.yellow + 'invalid json data in an item. ignored...' + ansi.reset)

        if self.is_quiet():
            pr.p('Finishing update...')
        ListUpdater.update_indexes({
            'cannot_read_file': self.empty_method,
            'invalid_json_data': self.empty_method,
        })

        pr.p(ansi.green + 'Done.' + ansi.reset)
