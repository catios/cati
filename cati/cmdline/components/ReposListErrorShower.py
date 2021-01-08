#
# ReposListErrorShower.py
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

""" shows repo config errors from list of repos """

from cati.cmdline import pr

def show(repos: list):
    """
    Shows errors in the repositories list

    Args:
        repos: list of loaded repositories (list[repo.Repo.Repo])
    """
    for repo in repos:
        if repo.syntax_errors:
            for error in repo.syntax_errors:
                pr.e(
                    'error in ' + repo.loaded_from_file + ':' + str(repo.line_number) + ': ' + error
                )
