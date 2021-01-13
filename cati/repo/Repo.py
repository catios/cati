#
# Repo.py
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

""" Cati repository model """

import os
import json
from cati.frontend import SysArch, Env
from .drivers.File import File as FileDriver
from .drivers.Http import Http as HttpDriver

class Repo:
    """ Cati repository model """
    def __init__(self, config: str):
        # ignore comments
        self.full_string = config.strip()
        config = config.strip().split(' ')
        self.url = config[0]
        self.syntax_errors = []
        self.successful_loaded = True
        config.pop(0)

        # set default values
        self.pkg = ['cati']
        self.arch = [SysArch.sys_arch()]
        self.channel = ['default']
        self.priority = 1
        self.is_disable = False
        self.name = None

        for item in config:
            item = item.strip()
            if item != '':
                parts = item.split('=')
                if len(parts) <= 1:
                    self.syntax_errors.append('undefined value for `' + parts[0] + '`')
                else:
                    if parts[0] == 'pkg':
                        self.pkg = parts[1].strip().split(',')
                        self.pkg = [tmp.strip() for tmp in self.pkg if tmp.strip() != '']
                    elif parts[0] == 'arch':
                        self.arch = parts[1].strip().split(',')
                        self.arch = [tmp.strip() for tmp in self.arch if tmp.strip() != '']
                    elif parts[0] == 'channel':
                        self.channel = parts[1].strip().split(',')
                        self.channel = [tmp.strip() for tmp in self.channel if tmp.strip() != '']
                    elif parts[0] == 'priority':
                        try:
                            self.priority = int(parts[1])
                        except:
                            pass
                    elif parts[0] == 'name':
                        self.name = parts[1]
                    elif parts[0] == 'disable':
                            self.is_disable = True
                    else:
                        self.syntax_errors.append('unknow option `' + parts[0] + '`')

        if self.name == None:
            self.name = self.pkg[0] + '-' + self.arch[0] + '-' + self.channel[0] + '-' + str(self.priority)
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
        """
        Test repository
        
        Returns:
            bool: True means connection is ok, False means not
        """
        return self.__driver.test()

    def get_data(self, download_event=None) -> str:
        """
        Recives repo data returns data as json

        Args:
            download_event (callable, None): if repo driver is http, this should be a function to download data

        Returns:
            str: repository data
        """
        data = self.__driver.get_data(download_event)
        try:
            j = json.loads(data)
            i = 0
            while i < len(j):
                try:
                    if not j[i]['arch'] in self.arch or not j[i]['pkg_type'] in self.pkg:
                        j.pop(i)
                except:
                    j.pop(i)
                i += 1
            data = json.dumps(j)
        except:
            pass
        data = json.loads(data)
        i = 0
        while i < len(data):
            try:
                tmp_channel = data[i]['channel']
                if self.channel != ['default']:
                    if not tmp_channel in self.channel:
                        data.pop(i)
                        continue
            except:
                pass
            data[i]['repo'] = self.name
            try:
                data[i]['file_size']
            except:
                data[i]['file_size'] = 0
            i += 1
        data = json.dumps(data)
        return data

    def get_pkg_str(self) -> str:
        """
        Returns self.pkg list (allowed package type of repo) as string

        Returns:
            str
        """
        s = ''
        for pkg in self.pkg:
            s += pkg + ','
        return s.strip(',')

    def get_arch_str(self) -> str:
        """
        Returns self.arch list (allowed package arch of repo) as string

        Returns:
            str
        """
        s = ''
        for arch in self.arch:
            s += arch + ','
        return s.strip(',')

    def get_channel_str(self) -> str:
        """
        Returns self.channel list (allowed version channels of repo) as string

        Returns:
            str
        """
        s = ''
        for channel in self.channel:
            s += channel + ','
        return s.strip(',')

    @staticmethod
    def get_list() -> list:
        """
        returns list of repositories
        
        Returns:
            list[Repo]: list of loaded repositories
        """
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
