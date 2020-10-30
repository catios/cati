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

""" List command """

from cmdline.BaseCommand import BaseCommand
from cmdline import pr, ansi
from package.Pkg import Pkg

class ListCommand(BaseCommand):
    """ List command """
    def help(self):
        """
        shows list of packages
        Options:
        --installed: show only installed packages
        --installed-manual: show only manual installed packages
        --author: filter packages list by author name. `--author='name of wanted author'` or more than 1 author: `--author='author 1 | author 2 | author 3'` (split with '|')
        --maintainer: filter packages list by maintainer name. `--maintainer='name of wanted maintainer'` or more than 1 author: `--maintainer='maintainer 1 | maintainer 2 | maintainer 3'` (split with '|')
        --category: filter packages list by category name. `--category='name of wanted category'` or more than 1 category: `--category='category 1 | category 2 | category 3'` (split with '|')
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'list',
            'options': {
                '--installed': [False, False],
                '--installed-manual': [False, False],
                '--quiet': [False, False],
                '-q': [False, False],
                '--verbose': [False, False],
                '-v': [False, False],
                '--author': [False, True],
                '--maintainer': [False, True],
                '--category': [False, True],
            },
            'max_args_count': 0,
            'min_args_count': 0,
        }

    def show_once(self, package: Pkg):
        """
        show once item in loaded packages list
        """
        if self.has_option('-q') or self.has_option('--quiet'):
            pr.p(package.data['name'])
            return
        output = ansi.green + package.data['name'] + ansi.reset + '/' +  ansi.yellow + package.data['version'] + ansi.reset
        if package.installed():
            if package.is_installed_manual(package.data['name']):
                output += '/Installed-Manual:' + ansi.blue + package.installed() + ansi.reset
            else:
                output += '/Installed:' + ansi.blue + package.installed() + ansi.reset
        output += '/[' + package.data['repo'] + ']'

        # if verbose output wanted, show first line of description
        if self.is_verbose():
            try:
                description_summary = package.data['description'].split('\n')[0]
                if description_summary != '':
                    output += '/ ' + ansi.header + description_summary + ansi.reset
            except:
                pass

        pr.p(output)

    def run(self):
        """ Run command """

        if not self.has_option('-q') and not self.has_option('--quiet'):
            pr.p('Loading packages list...')
            pr.p('========================')
        # load list of packages
        if self.has_option('--installed'):
            # just list installed packages
            packages = Pkg.installed_list()
        elif self.has_option('--installed-manual'):
            packages = Pkg.installed_list()
            packages_list = [tmp_pkg for tmp_pkg in packages['list'] if Pkg.is_installed_manual(tmp_pkg.data['name'])]
            packages['list'] = packages_list
        else:
            packages = Pkg.all_list()

        for error in packages['errors']:
            self.message(error + ansi.reset, True, before=ansi.red)

        # load filter options
        wanted_authors = []
        if self.has_option('--author'):
            wanted_authors = self.option_value('--author').strip().split('|')
            wanted_authors = [author.strip() for author in wanted_authors]
        wanted_maintainers = []
        if self.has_option('--maintainer'):
            wanted_maintainers = self.option_value('--maintainer').strip().split('|')
            wanted_maintainers = [maintainer.strip() for maintainer in wanted_maintainers]
        wanted_categories = []
        if self.has_option('--category'):
            wanted_categories = self.option_value('--category').strip().split('|')
            wanted_categories = [category.strip() for category in wanted_categories]

        for package in packages['list']:
            # check filters
            if wanted_authors:
                try:
                    if not package.data['author'].strip() in wanted_authors:
                        continue
                except:
                    continue
            if wanted_maintainers:
                try:
                    if not package.data['maintainer'].strip() in wanted_maintainers:
                        continue
                except:
                    continue
            if wanted_categories:
                try:
                    if not package.data['category'].strip() in wanted_categories:
                        continue
                except:
                    continue
            # show item
            self.show_once(package)
