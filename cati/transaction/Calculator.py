#
# Calculator.py
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

"""
Transaction calculator.

transaction calculator gets a list from packages for
install/remove/upgrade/downgrade operations
and calculates all of operations needed to be done
(actualy, includes dependencies, conflicts...)
"""

from cati.dotcati.Pkg import Pkg

class Calculator:
    """ Transaction calculator """
    def __init__(self, with_recommends=False):
        self.to_remove = []
        self.to_install = []
        self.with_recommends = with_recommends

    def has_any_thing(self):
        """ returns is there any transactions to do """
        return self.to_remove or self.to_install

    def get_total_download_size(self) -> int:
        """
        Returns total download size of packages

        Returns:
            int: the bytes count
        """

        total_size = 0

        for pkg in self.to_install:
            try:
                total_size += int(pkg.data['file_size'])
            except:
                pass

        return total_size

    def remove(self, pkgs: list):
        """ Add packages to remove """
        for pkg in pkgs:
            if pkg.installed():
                self.to_remove.append(pkg)
        self.refresh_lists()

    def get_sorted_list(self):
        """ returns sorted list of all of packages """
        new_list = []
        for item in self.to_remove:
            new_list.append(
                {
                    "action": "remove",
                    "pkg": item
                }
            )
        for item in self.to_install:
            new_list.append(
                {
                    "action": "install",
                    "pkg": item
                }
            )

        return new_list

    def install(self, pkgs: list):
        """ Add packages for install """
        for pkg in pkgs:
            try:
                tmp = pkg.wanted_version
            except:
                pkg.wanted_version = pkg.data['version']
            try:
                tmp = pkg.depend_get_next
            except:
                pkg.depend_get_next = {}
            try:
                tmp = pkg.conflict_get_next
            except:
                pkg.conflict_get_next = {}
            try:
                tmp = pkg.is_manual
            except:
                pkg.is_manual = False
            i = 0
            added = False
            while i < len(self.to_install):
                if self.to_install[i].data['name'] == pkg.wanted_version:
                    self.to_install[i] = pkg
                    added = True
                i += 1
            if not added:
                self.to_install.insert(0, pkg)
        self.refresh_lists()

    def handle_install_depends(self):
        """ Adds installable packages depends to install list """
        new_to_install = []
        i = 0
        while i < len(self.to_install):
            depends = self.to_install[i].get_depends()
            if self.with_recommends:
                depends = [*depends, *self.to_install[i].get_recommends()]
            for depend in depends:
                if not Pkg.check_state(depend) and depend.strip()[0] != '@':
                    # find package depend
                    try:
                        self.to_install[i].depend_get_next[depend]
                    except:
                        try:
                            self.to_install[i].depend_get_next[depend] = 0
                        except:
                            self.to_install[i].depend_get_next = {}
                            self.to_install[i].depend_get_next[depend] = 0
                    pkg = Pkg.check_state(depend, get_false_pkg=True, get_false_pkg_next=self.to_install[i].depend_get_next[depend])
                    self.to_install[i].depend_get_next[depend] += 1
                    if len(pkg) == 1:
                        a = 0
                        added = False
                        while a < len(self.to_install):
                            if self.to_install[a].data['name'] == pkg[0]:
                                added = True
                            a += 1
                        if not added:
                            new_to_install.append(Pkg.load_last(pkg[0]))
                    elif len(pkg) == 3:
                        a = 0
                        added = False
                        while a < len(self.to_install):
                            if self.to_install[a].data['name'] == pkg[0]:
                                wanted_version = pkg[2]
                                installed_version = self.to_install[a].wanted_version
                                if pkg[1] == '=':
                                    if Pkg.compare_version(installed_version, wanted_version) == 0:
                                        added = True
                                elif pkg[1] == '>=':
                                    if Pkg.compare_version(installed_version, wanted_version) >= 0:
                                        added = True
                                elif pkg[1] == '<=':
                                    if Pkg.compare_version(installed_version, wanted_version) <= 0:
                                        added = True
                                elif pkg[1] == '>':
                                    if Pkg.compare_version(installed_version, wanted_version) == 1:
                                        added = True
                                elif pkg[1] == '<':
                                    if Pkg.compare_version(installed_version, wanted_version) == -1:
                                        added = True
                            a += 1
                        if not added:
                            pkg_obj = None
                            if pkg[1] == '=':
                                pkg_obj = Pkg.load_version(pkg[0], pkg[2])
                            elif pkg[1] == '>=' or pkg[1] == '>':
                                pkg_obj = Pkg.load_last(pkg[0])
                            elif pkg[1] == '<=':
                                pkg_obj = Pkg.load_version(pkg[0], pkg[2])
                            elif pkg[1] == '<':
                                pkg_obj = Pkg.load_last(pkg[0])
                                versions = pkg_obj.get_versions_list()
                                x = 0
                                while x < len(versions):
                                    if Pkg.compare_version(versions[x][0], pkg[0]) >= 0:
                                        versions.pop(x)
                                    x += 1
                                versions = [v[0] for v in versions]
                                wanted_ver = pkg.get_last_version(versions)
                                pkg_obj = Pkg.load_version(pkg[0], wanted_ver)
                            new_to_install.append(pkg_obj)
            i += 1

        if new_to_install:
            self.install(new_to_install)

        self.handle_install_reverse_depends()

    def handle_install_reverse_depends(self):
        """ Adds installable packages reverse depends to install list """
        new_to_remove = []
        i = 0
        while i < len(self.to_install):
            reverse_depends = self.to_install[i].get_reverse_depends()
            for dep in reverse_depends:
                if dep.installed():
                    dep = Pkg.load_version(dep.data['name'], dep.installed())
                    for tmp_dep in dep.get_depends():
                        result = Pkg.check_state(tmp_dep, virtual={
                            'install': [
                                [
                                    self.to_install[i].data['name'], self.to_install[i].data['version']
                                ]
                            ],
                        })
                        if not result:
                            a = 0
                            added = False
                            while a < len(self.to_remove):
                                if self.to_remove[a].data['name'] == dep.data['name']:
                                    added = True
                                a += 1
                            if not added:
                                new_to_remove.append(dep)
            i += 1

        if new_to_remove:
            self.remove(new_to_remove)

    def handle_install_reverse_conflicts(self):
        """ Adds installable packages reverse conflicts to install list """
        new_to_remove = []
        i = 0
        while i < len(self.to_install):
            conflicts = self.to_install[i].get_reverse_conflicts()
            for conflict in conflicts:
                if conflict.installed():
                    a = 0
                    added = False
                    while a < len(self.to_remove):
                        if self.to_remove[a].data['name'] == conflict.data['name']:
                            added = True
                        a += 1
                    if not added:
                        new_to_remove.append(conflict)
            i += 1

        if new_to_remove:
            self.remove(new_to_remove)

    def handle_install_conflicts(self):
        """ Adds installable packages conflicts to install list """
        new_to_remove = []
        i = 0
        while i < len(self.to_install):
            conflicts = self.to_install[i].get_conflicts()
            for conflict in conflicts:
                if Pkg.check_state(conflict):
                    # find package conflict
                    try:
                        self.to_install[i].conflict_get_next[conflict]
                    except:
                        try:
                            self.to_install[i].conflict_get_next[conflict] = 0
                        except:
                            self.to_install[i].conflict_get_next = {}
                            self.to_install[i].conflict_get_next[conflict] = 0
                    pkg = Pkg.check_state(conflict, get_true_pkg=True, get_true_pkg_next=self.to_install[i].conflict_get_next[conflict])
                    self.to_install[i].conflict_get_next[conflict] += 1
                    a = 0
                    added = False
                    if type(pkg) == list:
                        while a < len(self.to_remove):
                            if self.to_remove[a].data['name'] == pkg[0]:
                                added = True
                            a += 1
                        if not added:
                            new_to_remove.append(Pkg.load_last(pkg[0]))
            i += 1

        if new_to_remove:
            self.remove(new_to_remove)
        
        self.handle_install_reverse_conflicts()

    def refresh_lists(self):
        """ Refresh packages list and sync them with depends and conflicts """
        # sync versions
        i = 0
        while i < len(self.to_remove):
            self.to_remove[i] = Pkg.load_version(self.to_remove[i].data['name'], self.to_remove[i].installed())
            i += 1
        i = 0
        while i < len(self.to_install):
            wv = self.to_install[i].wanted_version
            im = self.to_install[i].is_manual
            self.to_install[i] = Pkg.load_version(self.to_install[i].data['name'], self.to_install[i].wanted_version)
            self.to_install[i].wanted_version = wv
            self.to_install[i].is_manual = im
            i += 1

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
                if rd.installed():
                    if not rd.data['name'] in [tmp.data['name'] for tmp in self.to_remove]:
                        new_to_remove.append(rd)
        if new_to_remove:
            self.remove(new_to_remove)

        self.handle_install_depends()
        self.handle_install_conflicts()
