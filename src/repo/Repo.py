#
# Repo.py
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

""" Cati repository model """

import os
import json
from frontend import SysArch, Env
from repo.drivers.File import File as FileDriver
from repo.drivers.Http import Http as HttpDriver

class Repo:
    def __init__(self, config: str):
        # ignore comments
        self.full_string = config.strip()
        config = config.strip().split(' ')
        self.url = config[0]
        self.syntax_errors = []
        self.successful_loaded = True
        config.pop(0)

        # set default values
        self.pkg = 'main-repo'
        self.arch = SysArch.sys_arch()
        self.priority = 1
        self.name = self.pkg + '-' + self.arch + '@' + self.url

        for item in config:
            item = item.strip()
            if item != '':
                parts = item.split('=')
                if len(parts) <= 1:
                    self.syntax_errors.append('undefined value for `' + parts[0] + '`')
                else:
                    if parts[0] == 'pkg':
                        self.pkg = parts[1]
                    elif parts[0] == 'arch':
                        self.arch = parts[1]
                    elif parts[0] == 'priority':
                        try:
                            self.priority = int(parts[1])
                        except:
                            pass
                    elif parts[0] == 'name':
                        self.name = parts[1]
                    else:
                        self.syntax_errors.append('unknow option `' + parts[0] + '`')

        if self.name == 'Local' or self.name == 'local':
            self.name = self.name + '-repo'

        # initialize driver by url
        url_parts = self.url.strip().split('://', 1)
        if len(url_parts) <= 1:
            self.successful_loaded = False
            self.syntax_errors.append('invalid url')
            return
        # find driver
        driver_name = url_parts[0]
        if driver_name == 'file':
            self.__driver = FileDriver(url=self.url, pkg=self.pkg, arch=self.arch)
        elif driver_name in ['http', 'https']:
            self.__driver = HttpDriver(url=self.url, pkg=self.pkg, arch=self.arch)
        else:
            self.successful_loaded = False
            self.syntax_errors.append('invalid url type')
            return

    def test(self) -> bool:
        """ Test repository """
        return self.__driver.test()

    def get_data(self) -> str:
        """ Recives repo data returns data as json """
        data = self.__driver.get_data()
        try:
            j = json.loads(data)
            i = 0
            while i < len(j):
                j[i]['repo'] = self.name
                try:
                    if j[i]['arch'] != self.arch or j[i]['pkg_type'] != self.pkg:
                        j.pop(i)
                except:
                    pass
                i += 1
            data = json.dumps(j)
        except:
            pass
        return data

    @staticmethod
    def get_list():
        """ returns list of repositories """
        repos = []
        files = [Env.repos_config()]
        for item in os.listdir(Env.repos_config_dir()):
            if os.path.isfile(Env.repos_config_dir('/' + item)):
                files.append(Env.repos_config_dir('/' + item))
        for fl in files:
            f = open(fl, 'r')
            repos_content = f.read()
            f.close()
            lines = repos_content.split('\n')
            line_counter = 1
            for line in lines:
                line = line.split('#')[0].strip()
                line = line.strip()
                if line != '':
                    repo = Repo(line)
                    repo.line_number = line_counter
                    repo.loaded_from_file = fl
                    repos.append(repo)
                line_counter += 1

        # sort by priority
        sorted_repos = []
        while len(repos):
            i = 0
            while i < len(repos):
                is_less_than_all = True
                j = 0
                while j < len(repos):
                    if int(repos[i].priority) > int(repos[j].priority):
                        is_less_than_all = False
                    j += 1
                if is_less_than_all:
                    sorted_repos.append(repos[i])
                    repos.pop(i)
                i += 1

        return sorted_repos
