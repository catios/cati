#
# ListCommand.py
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

""" List command """

from cati.cmdline.BaseCommand import BaseCommand
from cati.cmdline import pr, ansi
from cati.dotcati.Pkg import Pkg

class ListCommand(BaseCommand):
    """ List command """
    def help(self):
        """
        shows list of packages

        Usage: cati list [options]

        Options:
        --installed: show only installed packages
        --installed-manual: show only manual installed packages
        --author=[author-name or author-nameS splited by `|`]: filter packages list by author name
        --maintainer=[maintainer-name or author-nameS splited by `|`]: filter packages list by maintainer name
        --category=[category-name or category-nameS splited by `|`]: filter packages list by category
        --search=[word]: search by packages name and description
        --upgradable: show list of upgradable packages
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
                '--upgradable': [False, False],
                '--author': [False, True],
                '--maintainer': [False, True],
                '--category': [False, True],
                '--search': [False, True],
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
                output += '/Installed-Manual:' + ansi.blue + package.installed().strip() + ansi.reset
            else:
                output += '/Installed:' + ansi.blue + package.installed().strip() + ansi.reset
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
        search_query = self.option_value('--search')
        if search_query:
            search_query_words = search_query.strip().split(' ')
            search_query_words = [word.strip() for word in search_query_words]
        else:
            search_query_words = []

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
            if search_query:
                is_math_with_query = False
                for word in search_query_words:
                    if word in package.data['name']:
                        is_math_with_query = True
                try:
                    if search_query in package.data['description']:
                        is_math_with_query = True
                except:
                    pass
                if not is_math_with_query:
                    continue

            if self.has_option('--upgradable'):
                if package.installed():
                    if Pkg.compare_version(package.data['version'], package.installed()) != 1:
                        continue
                else:
                    continue
            # show item
            self.show_once(package)
