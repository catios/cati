#
# Calculator.py
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

''' Transaction calculator '''

class Calculator:
    ''' Transaction calculator '''
    def __init__(self):
        self.to_remove = []

    def refresh_lists(self):
        ''' Refresh packages list and sync them with depends and conflicts '''
        # remove repeated lists in to_remove list
        a = 0
        while a < len(self.to_remove):
            b = 0
            while b < len(self.to_remove):
                if a != b:
                    if self.to_remove[a].data['name'] == self.to_remove[b].data['name']:
                        self.to_remove.pop(b)
                        a -= 1
                        b -= 1
                b += 1
            a += 1

        # sync to_remove list
        new_to_remove = []
        for item in self.to_remove:
            # load reverse dependnecy of current package and add them to list
            reverse_depends = item.get_reverse_depends()
            for rd in reverse_depends:
                if not rd.data['name'] in [tmp.data['name'] for tmp in self.to_remove]:
                    new_to_remove.append(rd)
        if new_to_remove:
            self.remove(new_to_remove)

    def remove(self, pkgs: list):
        ''' Add packages to remove '''
        for pkg in pkgs:
            if pkg.installed():
                self.to_remove.append(pkg)
        self.refresh_lists()

    def has_any_thing(self):
        return self.to_remove
