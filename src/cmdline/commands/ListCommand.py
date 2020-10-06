#
# ListCommand.py
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

''' List command '''

from cmdline.BaseCommand import BaseCommand
from cmdline import pr
from cmdline import ansi
from package.Pkg import Pkg

class ListCommand(BaseCommand):
    def help(self):
        '''
        shows list of packages

        this command shows list of available packages
        '''
        pass

    def define(self) -> dict:
        ''' Define and config this command '''
        return {
            'name': 'list',
            'options': {
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def show_once(self , package: Pkg):
        output = ansi.green + package.data['name'] + ansi.reset + '/' +  ansi.yellow + package.data['version'] + ansi.reset
        if package.installed():
            output += '/Installed:' + ansi.blue + package.installed() + ansi.reset
        output += '/[' + package.data['repo'] + ']'
        
        pr.p(output)

    def run(self):
        ''' Run command '''
        
        pr.p('Loading packages list...')
        pr.p('========================')
        # load list of packages
        if self.has_option('--installed'):
            # just list installed packages
            packages = Pkg.installed_list()
        else:
            packages = Pkg.all_list()

        for error in packages['errors']:
            self.message(ansi.red + error , True , before=ansi.reset)

        for package in packages['list']:
            self.show_once(package)
